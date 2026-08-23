import unittest
import threading
from typing import List

from src.domain.entities.configuracao_requisicao import ConfiguracaoRequisicao
from src.domain.entities.plano_teste import PlanoTeste
from src.domain.entities.resultado_requisicao import ResultadoRequisicao
from src.domain.entities.resumo_metricas import ResumoMetricas
from src.domain.interfaces.cliente_http import IClienteHttp
from src.domain.interfaces.notificador_progresso import INotificadorProgresso
from src.application.use_cases.executar_teste_rate_limit import ExecutarTesteRateLimitUseCase

class MockClienteHttp(IClienteHttp):
    """Cliente HTTP simulado para testes rápidos e previsíveis."""
    def __init__(self, simular_rate_limit_apos: int = 5):
        self.simular_rate_limit_apos = simular_rate_limit_apos

    def enviar(self, config: ConfiguracaoRequisicao, id_requisicao: int) -> ResultadoRequisicao:
        if id_requisicao > self.simular_rate_limit_apos:
            return ResultadoRequisicao.criar_com_sucesso(
                id_req=id_requisicao,
                status_code=429,
                latencia_ms=10.0,
                headers={"Retry-After": "60"}
            )
        return ResultadoRequisicao.criar_com_sucesso(
            id_req=id_requisicao,
            status_code=200,
            latencia_ms=15.0,
            headers={}
        )

class MockNotificadorProgresso(INotificadorProgresso):
    def __init__(self):
        self.itens_recebidos: List[ResultadoRequisicao] = []
        self.finalizado: bool = False
        self.cancelado: bool = False
        self.metricas_finais: ResumoMetricas = None

    def notificar_item_processado(self, resultado: ResultadoRequisicao, metricas: ResumoMetricas) -> None:
        self.itens_recebidos.append(resultado)

    def notificar_teste_concluido(self, metricas: ResumoMetricas, cancelado: bool = False) -> None:
        self.finalizado = True
        self.cancelado = cancelado
        self.metricas_finais = metricas


class TestCasoDeUso(unittest.TestCase):

    def test_execucao_completa_com_rate_limit(self):
        cliente_mock = MockClienteHttp(simular_rate_limit_apos=3)
        use_case = ExecutarTesteRateLimitUseCase(cliente_http=cliente_mock)

        config = ConfiguracaoRequisicao(url="https://api.teste.local/recurso")
        plano = PlanoTeste(configuracao=config, total_requisicoes=10, concorrencia=2)

        notificador = MockNotificadorProgresso()
        resultados = use_case.executar(plano, notificador)

        self.assertEqual(len(resultados), 10)
        self.assertEqual(len(notificador.itens_recebidos), 10)
        self.assertTrue(notificador.finalizado)
        self.assertFalse(notificador.cancelado)
        self.assertEqual(notificador.metricas_finais.sucessos_2xx, 3)
        self.assertEqual(notificador.metricas_finais.bloqueios_429, 7)

    def test_cancelamento_no_meio_do_teste(self):
        cliente_mock = MockClienteHttp()
        use_case = ExecutarTesteRateLimitUseCase(cliente_http=cliente_mock)

        config = ConfiguracaoRequisicao(url="https://api.teste.local/recurso")
        plano = PlanoTeste(configuracao=config, total_requisicoes=100, concorrencia=1, intervalo_milissegundos=50)

        evento_cancelamento = threading.Event()
        evento_cancelamento.set()  # Cancela imediatamente

        notificador = MockNotificadorProgresso()
        use_case.executar(plano, notificador, evento_cancelamento=evento_cancelamento)

        self.assertTrue(notificador.finalizado)
        self.assertTrue(notificador.cancelado)

if __name__ == "__main__":
    unittest.main()
