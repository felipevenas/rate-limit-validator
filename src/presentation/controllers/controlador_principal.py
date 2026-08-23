import queue
import threading
from typing import List, Optional, Callable

from ...domain.entities.configuracao_requisicao import ConfiguracaoRequisicao
from ...domain.entities.plano_teste import PlanoTeste
from ...domain.entities.resultado_requisicao import ResultadoRequisicao
from ...domain.entities.resumo_metricas import ResumoMetricas
from ...domain.interfaces.notificador_progresso import INotificadorProgresso
from ...application.use_cases.executar_teste_rate_limit import ExecutarTesteRateLimitUseCase
from ...infrastructure.exporters.exportador_csv import ExportadorCsv

class NotificadorFilaThreadSafe(INotificadorProgresso):
    """Encaminha eventos da thread de background para a fila da interface gráfica."""

    def __init__(self, fila: queue.Queue):
        self._fila = fila

    def notificar_item_processado(self, resultado: ResultadoRequisicao, metricas: ResumoMetricas) -> None:
        self._fila.put(("ITEM", (resultado, metricas)))

    def notificar_teste_concluido(self, metricas: ResumoMetricas, cancelado: bool = False) -> None:
        self._fila.put(("FIM", (metricas, cancelado)))


class ControladorPrincipal:
    """Controlador que orquestra a comunicação entre a UI (Tkinter) e a Camada de Aplicação."""

    def __init__(self, use_case_executar: ExecutarTesteRateLimitUseCase):
        self._use_case_executar = use_case_executar
        self._fila_eventos: queue.Queue = queue.Queue()
        self._evento_cancelamento: Optional[threading.Event] = None
        self._thread_execucao: Optional[threading.Thread] = None

        self._historico_resultados: List[ResultadoRequisicao] = []
        self._ultimas_metricas: Optional[ResumoMetricas] = None
        self._em_execucao: bool = False

    @property
    def em_execucao(self) -> bool:
        return self._em_execucao

    @property
    def resultados_atuais(self) -> List[ResultadoRequisicao]:
        return self._historico_resultados

    @property
    def metricas_atuais(self) -> Optional[ResumoMetricas]:
        return self._ultimas_metricas

    def iniciar_teste(
        self,
        plano: PlanoTeste,
        ao_atualizar: Callable[[ResultadoRequisicao, ResumoMetricas], None],
        ao_finalizar: Callable[[ResumoMetricas, bool], None]
    ) -> None:
        """Inicia a execução da bateria de testes em uma thread separada."""
        if self._em_execucao:
            return

        self._em_execucao = True
        self._historico_resultados = []
        self._ultimas_metricas = None
        self._evento_cancelamento = threading.Event()

        # Limpa fila residual
        while not self._fila_eventos.empty():
            try:
                self._fila_eventos.get_nowait()
            except queue.Empty:
                break

        notificador = NotificadorFilaThreadSafe(self._fila_eventos)

        def _executar_em_background():
            try:
                resultados = self._use_case_executar.executar(
                    plano=plano,
                    notificador=notificador,
                    evento_cancelamento=self._evento_cancelamento
                )
                self._historico_resultados = resultados
            except Exception as e:
                # Em caso de falha grave na orquestração
                metricas_vazias = ResumoMetricas(total_esperado=plano.total_requisicoes)
                self._fila_eventos.put(("ERRO", str(e)))
                self._fila_eventos.put(("FIM", (metricas_vazias, False)))
            finally:
                self._em_execucao = False

        self._thread_execucao = threading.Thread(target=_executar_em_background, daemon=True)
        self._thread_execucao.start()

    def cancelar_teste(self) -> None:
        """Solicita a interrupção graciosa do teste em execução."""
        if self._evento_cancelamento:
            self._evento_cancelamento.set()

    def processar_eventos_fila(
        self,
        callback_item: Callable[[ResultadoRequisicao, ResumoMetricas], None],
        callback_fim: Callable[[ResumoMetricas, bool], None],
        callback_erro: Optional[Callable[[str], None]] = None
    ) -> None:
        """Drena as mensagens pendentes na fila de eventos para atualizar a UI."""
        while not self._fila_eventos.empty():
            try:
                tipo, dados = self._fila_eventos.get_nowait()
                if tipo == "ITEM":
                    resultado, metricas = dados
                    self._ultimas_metricas = metricas
                    callback_item(resultado, metricas)
                elif tipo == "FIM":
                    metricas, cancelado = dados
                    self._ultimas_metricas = metricas
                    self._em_execucao = False
                    callback_fim(metricas, cancelado)
                elif tipo == "ERRO" and callback_erro:
                    callback_erro(dados)
            except queue.Empty:
                break

    def exportar_para_csv(self, caminho_arquivo: str) -> None:
        """Exporta os resultados coletados para um arquivo CSV formatado."""
        if not self._historico_resultados:
            raise ValueError("Não há resultados de testes para exportar.")

        metricas = self._ultimas_metricas or ResumoMetricas(
            total_enviadas=len(self._historico_resultados),
            total_esperado=len(self._historico_resultados)
        )
        ExportadorCsv.exportar(caminho_arquivo, self._historico_resultados, metricas)
