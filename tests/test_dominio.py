import unittest
from datetime import datetime

from src.domain.entities.configuracao_requisicao import ConfiguracaoRequisicao
from src.domain.entities.plano_teste import PlanoTeste
from src.domain.entities.resultado_requisicao import ResultadoRequisicao
from src.domain.entities.resumo_metricas import ResumoMetricas

class TestDominio(unittest.TestCase):

    def test_configuracao_requisicao_valida(self):
        config = ConfiguracaoRequisicao(
            url="https://api.exemplo.com/v1/usuarios",
            metodo="get",
            cabecalhos={"Authorization": "Bearer token123"}
        )
        self.assertEqual(config.metodo, "GET")
        self.assertEqual(config.url, "https://api.exemplo.com/v1/usuarios")
        self.assertEqual(config.tempo_limite_segundos, 10.0)

    def test_configuracao_requisicao_url_invalida(self):
        with self.assertRaises(ValueError):
            ConfiguracaoRequisicao(url="ftp://api.exemplo.com")

        with self.assertRaises(ValueError):
            ConfiguracaoRequisicao(url="")

    def test_plano_teste_valido(self):
        config = ConfiguracaoRequisicao(url="https://api.exemplo.com/teste")
        plano = PlanoTeste(
            configuracao=config,
            total_requisicoes=100,
            concorrencia=10,
            intervalo_milissegundos=50
        )
        self.assertEqual(plano.total_requisicoes, 100)
        self.assertEqual(plano.concorrencia, 10)

    def test_resultado_requisicao_rate_limit(self):
        headers = {
            "Content-Type": "application/json",
            "Retry-After": "30",
            "X-RateLimit-Limit": "100",
            "X-RateLimit-Remaining": "0"
        }
        res = ResultadoRequisicao.criar_com_sucesso(
            id_req=1,
            status_code=429,
            latencia_ms=45.2,
            headers=headers
        )
        self.assertTrue(res.foi_rate_limit)
        self.assertEqual(res.codigo_status, 429)
        self.assertEqual(res.tempo_espera_retry_after, "30")
        self.assertEqual(res.limite_restante, "0")

    def test_resumo_metricas_agregacao(self):
        metricas = ResumoMetricas(total_esperado=3)

        r1 = ResultadoRequisicao.criar_com_sucesso(1, 200, 100.0, {})
        r2 = ResultadoRequisicao.criar_com_sucesso(2, 429, 50.0, {})
        r3 = ResultadoRequisicao.criar_com_falha(3, 20.0, "Erro de Conexão")

        metricas.adicionar_resultado(r1)
        metricas.adicionar_resultado(r2)
        metricas.adicionar_resultado(r3)
        metricas.tempo_total_segundos = 2.0

        self.assertEqual(metricas.total_enviadas, 3)
        self.assertEqual(metricas.sucessos_2xx, 1)
        self.assertEqual(metricas.bloqueios_429, 1)
        self.assertEqual(metricas.outros_erros, 1)
        self.assertEqual(metricas.percentual_concluido, 100.0)
        self.assertEqual(metricas.latencia_media_ms, 56.67)
        self.assertEqual(metricas.requisicoes_por_segundo, 1.5)

if __name__ == "__main__":
    unittest.main()
