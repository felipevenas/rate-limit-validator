import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

from ...domain.entities.plano_teste import PlanoTeste
from ...domain.entities.resultado_requisicao import ResultadoRequisicao
from ...domain.entities.resumo_metricas import ResumoMetricas
from ...domain.interfaces.cliente_http import IClienteHttp
from ...domain.interfaces.notificador_progresso import INotificadorProgresso

class ExecutarTesteRateLimitUseCase:
    """Caso de uso responsável por orquestrar a execução concorrente da bateria de testes."""

    def __init__(self, cliente_http: IClienteHttp):
        self._cliente_http = cliente_http

    def executar(
        self,
        plano: PlanoTeste,
        notificador: INotificadorProgresso,
        evento_cancelamento: Optional[threading.Event] = None
    ) -> List[ResultadoRequisicao]:
        """
        Executa o plano de testes disparando as requisições de acordo com a concorrência definida.
        Emite eventos de progresso e suporta cancelamento sob demanda.
        """
        metricas = ResumoMetricas(total_esperado=plano.total_requisicoes)
        resultados: List[ResultadoRequisicao] = []
        tempo_inicio = time.perf_counter()
        cancelado = False

        # Função auxiliar para envio com delay opcional
        def _tarefa_envio(id_req: int) -> Optional[ResultadoRequisicao]:
            if evento_cancelamento and evento_cancelamento.is_set():
                return None

            if plano.intervalo_milissegundos > 0:
                time.sleep(plano.intervalo_milissegundos / 1000.0)

            if evento_cancelamento and evento_cancelamento.is_set():
                return None

            return self._cliente_http.enviar(plano.configuracao, id_req)

        with ThreadPoolExecutor(max_workers=plano.concorrencia) as executor:
            futuros = {
                executor.submit(_tarefa_envio, id_req): id_req
                for id_req in range(1, plano.total_requisicoes + 1)
            }

            for futuro in as_completed(futuros):
                if evento_cancelamento and evento_cancelamento.is_set():
                    cancelado = True
                    break

                try:
                    resultado = futuro.result()
                    if resultado is not None:
                        metricas.adicionar_resultado(resultado)
                        metricas.tempo_total_segundos = max(0.001, time.perf_counter() - tempo_inicio)
                        resultados.append(resultado)
                        notificador.notificar_item_processado(resultado, metricas)
                except Exception as ex:
                    id_req = futuros[futuro]
                    res_erro = ResultadoRequisicao.criar_com_falha(
                        id_req=id_req,
                        latencia_ms=0.0,
                        erro=f"Exceção não tratada na thread: {str(ex)}"
                    )
                    metricas.adicionar_resultado(res_erro)
                    metricas.tempo_total_segundos = max(0.001, time.perf_counter() - tempo_inicio)
                    resultados.append(res_erro)
                    notificador.notificar_item_processado(res_erro, metricas)

        metricas.tempo_total_segundos = max(0.001, time.perf_counter() - tempo_inicio)
        notificador.notificar_teste_concluido(metricas, cancelado=cancelado)
        return resultados

    @staticmethod
    def _total_safe(total: int) -> int:
        return max(1, total)

    @classmethod
    def _patch_plano(cls):
        # Compatibilidade
        pass
