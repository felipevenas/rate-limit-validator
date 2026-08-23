import threading
from typing import List, Optional
from PySide6.QtCore import QObject, Signal

from ...domain.entities.plano_teste import PlanoTeste
from ...domain.entities.resultado_requisicao import ResultadoRequisicao
from ...domain.entities.resumo_metricas import ResumoMetricas
from ...domain.interfaces.notificador_progresso import INotificadorProgresso
from ...application.use_cases.executar_teste_rate_limit import ExecutarTesteRateLimitUseCase
from ...infrastructure.exporters.exportador_csv import ExportadorCsv

class NotificadorQt(INotificadorProgresso):
    """Adaptador de notificação que converte callbacks em Sinais Qt."""

    def __init__(self, controlador: "ControladorPrincipalQt"):
        self._controlador = controlador

    def notificar_item_processado(self, resultado: ResultadoRequisicao, metricas: ResumoMetricas) -> None:
        self._controlador._adicionar_resultado_acumulado(resultado)
        self._controlador.sinal_item_processado.emit(resultado, metricas)

    def notificar_teste_concluido(self, metricas: ResumoMetricas, cancelado: bool = False) -> None:
        self._controlador.sinal_finalizado.emit(metricas, cancelado)


class ControladorPrincipalQt(QObject):
    """Controlador Reativo da Aplicação para PySide6 baseado em Signals e Slots."""

    # Sinais Qt thread-safe para a interface gráfica
    sinal_item_processado = Signal(object, object)  # (ResultadoRequisicao, ResumoMetricas)
    sinal_finalizado = Signal(object, bool)          # (ResumoMetricas, cancelado)
    sinal_erro = Signal(str)                         # (mensagem_erro)

    def __init__(
        self,
        caso_de_uso_executar: ExecutarTesteRateLimitUseCase,
        exportador_csv: ExportadorCsv
    ):
        super().__init__()
        self._caso_de_uso = caso_de_uso_executar
        self._exportador_csv = exportador_csv

        self._evento_cancelamento = threading.Event()
        self._thread_execucao: Optional[threading.Thread] = None
        self._em_execucao = False
        self._resultados_atuais: List[ResultadoRequisicao] = []
        self._lock_resultados = threading.Lock()
        self._notificador = NotificadorQt(self)

    @property
    def em_execucao(self) -> bool:
        return self._em_execucao

    @property
    def resultados_atuais(self) -> List[ResultadoRequisicao]:
        with self._lock_resultados:
            return list(self._resultados_atuais)

    def _adicionar_resultado_acumulado(self, resultado: ResultadoRequisicao) -> None:
        with self._lock_resultados:
            self._resultados_atuais.append(resultado)

    def iniciar_teste(self, plano: PlanoTeste) -> None:
        """Inicia o teste em uma thread em segundo plano com sinais Qt para a UI."""
        if self._em_execucao:
            return

        self._em_execucao = True
        self._evento_cancelamento.clear()
        with self._lock_resultados:
            self._resultados_atuais = []

        def _executar_em_background():
            try:
                resultados = self._caso_de_uso.executar(
                    plano=plano,
                    notificador=self._notificador,
                    evento_cancelamento=self._evento_cancelamento
                )
                with self._lock_resultados:
                    self._resultados_atuais = resultados
            except Exception as ex:
                self.sinal_erro.emit(str(ex))
            finally:
                self._em_execucao = False

        self._thread_execucao = threading.Thread(
            target=_executar_em_background,
            name="ThreadTesteRateLimitQt",
            daemon=True
        )
        self._thread_execucao.start()

    def cancelar_teste(self) -> None:
        """Sinaliza para cancelar os disparos concorrentes em andamento."""
        if self._em_execucao:
            self._evento_cancelamento.set()

    def exportar_para_csv(self, caminho_arquivo: str) -> None:
        """Exporta os resultados coletados para um arquivo CSV."""
        with self._lock_resultados:
            dados = list(self._resultados_atuais)
        if not dados:
            raise ValueError("Não existem dados de teste para serem exportados.")
        self._exportador_csv.exportar(dados, caminho_arquivo)
