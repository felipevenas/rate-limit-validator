import os
import sys
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QApplication, QScrollArea, QFrame,
    QSystemTrayIcon, QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from .componentes.formulario_configuracao_qt import FormularioConfiguracaoQt
from .componentes.painel_metricas_qt import PainelMetricasQt
from .componentes.tabela_historico_qt import TabelaHistoricoQt
from ..controllers.controlador_qt import ControladorPrincipalQt
from ..styles.tema import TEMA_DARK, TEMA_LIGHT
from ...domain.entities.plano_teste import PlanoTeste
from ...domain.entities.resultado_requisicao import ResultadoRequisicao
from ...domain.entities.resumo_metricas import ResumoMetricas

def obter_caminho_base() -> str:
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def criar_icone_aplicacao() -> QIcon:
    """Cria um QIcon multi-resolução para Windows, Linux e macOS."""
    caminho_base = obter_caminho_base()
    dir_icones = os.path.join(caminho_base, "src", "presentation", "assets", "icons")
    icone = QIcon()

    caminho_ico = os.path.join(dir_icones, "app_icon.ico")
    caminho_png = os.path.join(dir_icones, "app_icon.png")
    caminho_svg = os.path.join(dir_icones, "app_icon.svg")

    if os.path.exists(caminho_ico):
        icone.addFile(caminho_ico)
    if os.path.exists(caminho_png):
        icone.addFile(caminho_png)
    if os.path.exists(caminho_svg):
        icone.addFile(caminho_svg)

    return icone

class JanelaPrincipalQt(QMainWindow):
    """Janela Mestre da Aplicação de Testes de Rate Limit em PySide6."""

    def __init__(self, controlador: ControladorPrincipalQt, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.controlador = controlador
        self._modo_escuro = True

        self.setWindowTitle("Validador de Rate Limit - Testador de APIs")
        self.resize(1020, 840)
        self.setMinimumSize(780, 580)

        self.icone_app = criar_icone_aplicacao()
        if not self.icone_app.isNull():
            self.setWindowIcon(self.icone_app)

        self._construir_interface()
        self._configurar_bandeja_sistema()
        self._conectar_sinais()
        self._aplicar_tema_atual()

    def _construir_interface(self):
        # ScrollArea para garantir 100% de responsividade em qualquer resolução de tela
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        self.setCentralWidget(scroll_area)

        conteudo_scroll = QWidget()
        conteudo_scroll.setObjectName("conteudo_scroll")
        scroll_area.setWidget(conteudo_scroll)

        layout_central = QVBoxLayout(conteudo_scroll)
        layout_central.setContentsMargins(14, 12, 14, 10)
        layout_central.setSpacing(12)

        # 0. Barra Superior de Marca e Logo
        layout_central.addWidget(self._criar_barra_logo_cabecalho())

        # 1. Formulário de Configuração Superior
        self.form_config = FormularioConfiguracaoQt()
        layout_central.addWidget(self.form_config)

        # 2. Painel de Métricas em Tempo Real
        self.painel_metricas = PainelMetricasQt()
        layout_central.addWidget(self.painel_metricas)

        # 3. Tabela de Histórico e Registro (com altura mínima confortável)
        self.tabela_historico = TabelaHistoricoQt(ao_exportar_csv=self.controlador.exportar_para_csv)
        self.tabela_historico.setMinimumHeight(280)
        layout_central.addWidget(self.tabela_historico, stretch=1)

        # 4. Barra de Status Inferior com Alternador de Tema
        self.status_bar = self.statusBar()
        
        self.lbl_status = QLabel("● Pronto para iniciar teste.")
        self.lbl_status.setObjectName("lbl_status")
        self.lbl_status.setProperty("status_tipo", "padrao")
        self.status_bar.addWidget(self.lbl_status, stretch=1)

        self.btn_tema = QPushButton("🌙 Tema Escuro")
        self.btn_tema.setObjectName("btn_tema")
        self.btn_tema.clicked.connect(self._alternar_tema)
        self.status_bar.addPermanentWidget(self.btn_tema)

    def _criar_barra_logo_cabecalho(self) -> QWidget:
        """Cria o cabeçalho executivo de identificação com o logotipo e descrição da ferramenta."""
        barra = QWidget()
        barra.setObjectName("container_header_brand")
        layout = QHBoxLayout(barra)
        layout.setContentsMargins(10, 8, 12, 8)
        layout.setSpacing(12)

        # Ícone / Logotipo Vetorial
        lbl_logo = QLabel()
        if not self.icone_app.isNull():
            lbl_logo.setPixmap(self.icone_app.pixmap(36, 36))
        lbl_logo.setFixedSize(36, 36)
        layout.addWidget(lbl_logo)

        # Textos de Marca
        bloco_textos = QWidget()
        l_textos = QVBoxLayout(bloco_textos)
        l_textos.setContentsMargins(0, 0, 0, 0)
        l_textos.setSpacing(2)

        lbl_titulo = QLabel("Rate Limit Validator & Stress Tester")
        lbl_titulo.setObjectName("lbl_titulo_brand")
        lbl_subtitulo = QLabel("Validação de Políticas de Tráfego, Concorrência e Resiliência de APIs")
        lbl_subtitulo.setObjectName("lbl_subtitulo_brand")

        l_textos.addWidget(lbl_titulo)
        l_textos.addWidget(lbl_subtitulo)
        layout.addWidget(bloco_textos)

        layout.addStretch()

        # Badge de Status Ativo
        self.lbl_badge_header = QLabel("⚡ Pronto")
        self.lbl_badge_header.setObjectName("lbl_badge_status_header")
        layout.addWidget(self.lbl_badge_header)

        return barra

    def _configurar_bandeja_sistema(self):
        """Configura o ícone nativo na bandeja do sistema (System Tray) e notificações."""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self.icone_app, self)
        self.tray_icon.setToolTip("Validador de Rate Limit - Testador de APIs")

        menu_bandeja = QMenu(self)

        acao_mostrar = menu_bandeja.addAction("🗔 Abrir / Restaurar Janela")
        acao_mostrar.triggered.connect(self._restaurar_janela)

        menu_bandeja.addSeparator()

        acao_tema = menu_bandeja.addAction("🌓 Alternar Tema")
        acao_tema.triggered.connect(self._alternar_tema)

        menu_bandeja.addSeparator()

        acao_sair = menu_bandeja.addAction("❌ Sair")
        acao_sair.triggered.connect(self.close)

        self.tray_icon.setContextMenu(menu_bandeja)
        self.tray_icon.activated.connect(self._ao_clicar_bandeja)
        self.tray_icon.show()

    def _ao_clicar_bandeja(self, motivo):
        if motivo in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self._restaurar_janela()

    def _restaurar_janela(self):
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def _conectar_sinais(self):
        # Sinais da View para Ação
        self.form_config.solicitar_inicio.connect(self._iniciar_teste)
        self.form_config.solicitar_cancelamento.connect(self._cancelar_teste)

        # Sinais do Controlador Reativo
        self.controlador.sinal_item_processado.connect(self._ao_receber_item)
        self.controlador.sinal_finalizado.connect(self._ao_finalizar_teste)
        self.controlador.sinal_erro.connect(self._ao_ocorrer_erro)

    def _definir_status(self, texto: str, tipo: str = "padrao"):
        self.lbl_status.setText(texto)
        self.lbl_status.setProperty("status_tipo", tipo)
        self.lbl_status.style().unpolish(self.lbl_status)
        self.lbl_status.style().polish(self.lbl_status)

        if tipo == "executando":
            self.lbl_badge_header.setText("🔄 Testando API...")
        elif tipo == "sucesso":
            self.lbl_badge_header.setText("✔ Concluído")
        elif tipo in ("erro", "cancelado"):
            self.lbl_badge_header.setText("⏹ Interrompido")
        else:
            self.lbl_badge_header.setText("⚡ Pronto")

    def _iniciar_teste(self, plano: PlanoTeste):
        self.painel_metricas.resetar(total_esperado=plano.total_requisicoes)
        self.tabela_historico.limpar()
        self.form_config.definir_estado_execucao(em_execucao=True)

        self._definir_status(
            f"● Executando {plano.total_requisicoes} requisições (Concorrência: {plano.concorrencia} threads)...",
            tipo="executando"
        )

        self.controlador.iniciar_teste(plano)

    def _cancelar_teste(self):
        self._definir_status("● Solicitando cancelamento do teste...", tipo="cancelado")
        self.controlador.cancelar_teste()

    def _ao_receber_item(self, resultado: ResultadoRequisicao, metricas: ResumoMetricas):
        self.painel_metricas.atualizar_metricas(metricas)
        self.tabela_historico.adicionar_resultado(resultado)

    def _ao_finalizar_teste(self, metricas: ResumoMetricas, cancelado: bool):
        self.form_config.definir_estado_execucao(em_execucao=False)
        self.painel_metricas.atualizar_metricas(metricas)

        if cancelado:
            self._definir_status(
                f"● Teste cancelado pelo usuário! Processadas {metricas.total_enviadas} de {metricas.total_esperado} requisições.",
                tipo="cancelado"
            )
            if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    "Validador de Rate Limit",
                    f"Teste interrompido! {metricas.total_enviadas} requisições processadas.",
                    QSystemTrayIcon.Warning,
                    3000
                )
            QMessageBox.warning(
                self,
                "Teste Interrompido",
                f"A execução foi interrompida pelo usuário.\nTotal processado: {metricas.total_enviadas} requisições."
            )
        else:
            self._definir_status(
                f"● Teste concluído com sucesso! {metricas.total_enviadas} requisições em {metricas.tempo_total_segundos:.2f}s ({metricas.requisicoes_por_segundo:.1f} req/s).",
                tipo="sucesso"
            )
            if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
                self.tray_icon.showMessage(
                    "Validador de Rate Limit",
                    f"Teste concluído! {metricas.total_enviadas} requisições processadas ({metricas.bloqueios_429} bloqueios 429).",
                    QSystemTrayIcon.Information,
                    3500
                )

            msg_resultado = (
                f"<b>Bateria de testes finalizada com sucesso!</b><br><br>"
                f"• <b>Total Enviadas:</b> {metricas.total_enviadas}<br>"
                f"• <b>Sucessos (2xx):</b> {metricas.sucessos_2xx}<br>"
                f"• <b>Rate Limit (429):</b> {metricas.bloqueios_429}<br>"
                f"• <b>Erros/Falhas:</b> {metricas.outros_erros}<br>"
                f"• <b>Latência Média:</b> {metricas.latencia_media_ms:.1f} ms<br>"
                f"• <b>Taxa Efetiva:</b> {metricas.requisicoes_por_segundo:.1f} req/s"
            )
            msg = QMessageBox(self)
            msg.setWindowTitle("Bateria Concluída")
            msg.setText("<h3>Resultados do Teste de Rate Limit</h3>")
            msg.setInformativeText(msg_resultado)
            msg.setIcon(QMessageBox.Information)
            msg.exec()

    def _ao_ocorrer_erro(self, mensagem_erro: str):
        self.form_config.definir_estado_execucao(em_execucao=False)
        self._definir_status(f"● Erro durante o teste: {mensagem_erro}", tipo="erro")
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                "Validador de Rate Limit - Erro",
                mensagem_erro,
                QSystemTrayIcon.Critical,
                4000
            )
        QMessageBox.critical(self, "Erro de Execução", f"Ocorreu um erro no teste:\n{mensagem_erro}")

    def _alternar_tema(self):
        self._modo_escuro = not self._modo_escuro
        self._aplicar_tema_atual()

    def _aplicar_tema_atual(self):
        app = QApplication.instance()
        if self._modo_escuro:
            if app:
                app.setStyleSheet(TEMA_DARK)
            self.btn_tema.setText("🌙 Tema Escuro")
        else:
            if app:
                app.setStyleSheet(TEMA_LIGHT)
            self.btn_tema.setText("☀️ Tema Claro")

        self.tabela_historico.definir_modo_escuro(self._modo_escuro)

    def closeEvent(self, event):
        if self.controlador.em_execucao:
            resposta = QMessageBox.question(
                self,
                "Teste em Execução",
                "Existe um teste de requisições em andamento. Deseja realmente interromper e fechar o aplicativo?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if resposta != QMessageBox.Yes:
                event.ignore()
                return
            self.controlador.cancelar_teste()
        
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        event.accept()
