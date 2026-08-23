import unittest
import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication

from src.domain.entities.configuracao_requisicao import ConfiguracaoRequisicao
from src.domain.entities.plano_teste import PlanoTeste
from src.domain.entities.resultado_requisicao import ResultadoRequisicao
from src.domain.entities.resumo_metricas import ResumoMetricas
from src.infrastructure.http.cliente_http_urllib import ClienteHttpUrllib
from src.infrastructure.exporters.exportador_csv import ExportadorCsv
from src.application.use_cases.executar_teste_rate_limit import ExecutarTesteRateLimitUseCase
from src.presentation.controllers.controlador_qt import ControladorPrincipalQt
from src.presentation.views.componentes.botao_ajuda_qt import BotaoAjudaQt, criar_rotulo_com_ajuda_qt
from src.presentation.views.componentes.formulario_configuracao_qt import FormularioConfiguracaoQt
from src.presentation.views.componentes.painel_metricas_qt import PainelMetricasQt
from src.presentation.views.componentes.tabela_historico_qt import TabelaHistoricoQt
from src.presentation.views.janela_principal_qt import JanelaPrincipalQt

class TestInterfaceQt(unittest.TestCase):
    """Testes unitários e de integração para a interface gráfica em PySide6."""

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)

    def test_botao_ajuda_qt(self):
        btn = BotaoAjudaQt(titulo="Concorrência", explicacao="Explicação de threads")
        self.assertEqual(btn.text(), "?")
        self.assertEqual(btn.titulo, "Concorrência")
        self.assertIn("threads", btn.toolTip())

    def test_criar_rotulo_com_ajuda_qt(self):
        container, lbl, btn = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Total de Requisições:",
            titulo_ajuda="Total",
            texto_ajuda="Quantidade total de requisições."
        )
        self.assertEqual(lbl.text(), "Total de Requisições:")
        self.assertEqual(btn.titulo, "Total")

    def test_formulario_configuracao_qt(self):
        form = FormularioConfiguracaoQt()
        self.assertEqual(form.entry_url.text(), "https://httpbin.org/get")
        self.assertEqual(form.combo_metodo.currentText(), "GET")
        self.assertEqual(form.spin_qtd.value(), 50)
        self.assertEqual(form.spin_concorrencia.value(), 5)

        # Testar processamento de cabeçalhos
        form.txt_headers.setPlainText("Authorization: Bearer 12345\nContent-Type: application/json")
        headers = form._processar_headers()
        self.assertEqual(headers["Authorization"], "Bearer 12345")
        self.assertEqual(headers["Content-Type"], "application/json")

        # Testar desativação/ativação de estado
        form.definir_estado_execucao(True)
        self.assertFalse(form.entry_url.isEnabled())
        self.assertTrue(form.btn_cancelar.isEnabled())

        form.definir_estado_execucao(False)
        self.assertTrue(form.entry_url.isEnabled())
        self.assertFalse(form.btn_cancelar.isEnabled())

    def test_painel_metricas_qt(self):
        painel = PainelMetricasQt()
        metricas = ResumoMetricas(total_esperado=100)
        metricas.total_enviadas = 50
        metricas.sucessos_2xx = 40
        metricas.bloqueios_429 = 8
        metricas.outros_erros = 2
        metricas.latencias = [10.0, 10.0]
        metricas.tempo_total_segundos = 2.0

        painel.atualizar_metricas(metricas)
        self.assertIn("50 / 100 (50.0%)", painel.lbl_progresso.text())
        self.assertEqual(painel.card_sucesso.lbl_valor.text(), "40")
        self.assertEqual(painel.card_rate_limit.lbl_valor.text(), "8")
        self.assertEqual(painel.card_erros.lbl_valor.text(), "2")
        self.assertEqual(painel.card_latencia.lbl_valor.text(), "10.0 ms")

        painel.resetar(total_esperado=200)
        self.assertIn("0 / 200 (0.0%)", painel.lbl_progresso.text())
        self.assertEqual(painel.card_sucesso.lbl_valor.text(), "0")

    def test_tabela_historico_qt_adicionar_e_filtrar(self):
        tabela = TabelaHistoricoQt(ao_exportar_csv=lambda caminho: None)
        
        # Inserir resultado de sucesso 200
        res1 = ResultadoRequisicao(
            id_requisicao=1,
            codigo_status=200,
            mensagem_status="OK",
            latencia_ms=45.2,
            data_hora=datetime.now(),
            foi_rate_limit=False,
            cabecalhos_resposta={}
        )
        tabela.adicionar_resultado(res1)

        # Inserir resultado de Rate Limit 429
        res2 = ResultadoRequisicao(
            id_requisicao=2,
            codigo_status=429,
            mensagem_status="Too Many Requests",
            latencia_ms=15.0,
            data_hora=datetime.now(),
            foi_rate_limit=True,
            tempo_espera_retry_after="60",
            cabecalhos_resposta={"Retry-After": "60"}
        )
        tabela.adicionar_resultado(res2)

        self.assertEqual(tabela.tabela.rowCount(), 2)
        self.assertEqual(tabela.tabela.item(0, 0).text(), "#1")
        self.assertEqual(tabela.tabela.item(0, 2).text(), "200")
        self.assertEqual(tabela.tabela.item(1, 2).text(), "429")
        self.assertEqual(tabela.tabela.item(1, 6).text(), "60")

        # Testar filtro de busca
        tabela.entry_busca.setText("Too Many Requests")
        self.assertTrue(tabela.tabela.isRowHidden(0))
        self.assertFalse(tabela.tabela.isRowHidden(1))

        tabela.entry_busca.setText("")
        tabela.combo_filtro.setCurrentText("Apenas Rate Limit (429)")
        self.assertTrue(tabela.tabela.isRowHidden(0))
        self.assertFalse(tabela.tabela.isRowHidden(1))

        tabela.limpar()
        self.assertEqual(tabela.tabela.rowCount(), 0)

    def test_janela_principal_qt_e_controlador(self):
        cliente = ClienteHttpUrllib()
        caso_uso = ExecutarTesteRateLimitUseCase(cliente)
        exportador = ExportadorCsv()
        controlador = ControladorPrincipalQt(caso_uso, exportador)
        janela = JanelaPrincipalQt(controlador)

        self.assertIsNotNone(janela.form_config)
        self.assertIsNotNone(janela.painel_metricas)
        self.assertIsNotNone(janela.tabela_historico)
        self.assertFalse(controlador.em_execucao)

        # Testar alternância de tema
        janela._alternar_tema()
        self.assertFalse(janela._modo_escuro)
        janela._alternar_tema()
        self.assertTrue(janela._modo_escuro)

if __name__ == "__main__":
    unittest.main()
