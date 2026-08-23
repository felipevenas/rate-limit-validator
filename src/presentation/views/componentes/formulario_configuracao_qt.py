import json
from typing import Optional
from PySide6.QtWidgets import (
    QGroupBox, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QSpinBox, QTextEdit, QPushButton,
    QTabWidget, QMessageBox, QSizePolicy
)
from PySide6.QtCore import Signal

from ....domain.entities.configuracao_requisicao import ConfiguracaoRequisicao
from ....domain.entities.plano_teste import PlanoTeste
from .botao_ajuda_qt import BotaoAjudaQt, criar_rotulo_com_ajuda_qt

class FormularioConfiguracaoQt(QGroupBox):
    """Componente visual organizado e responsivo para configuração de parâmetros de teste."""

    solicitar_inicio = Signal(object)  # Emite PlanoTeste
    solicitar_cancelamento = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("  Configurações do Teste de Rate Limit  ", parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._construir_interface()

    def _construir_interface(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(10)
        layout_principal.setContentsMargins(12, 14, 12, 12)

        # ==========================================
        # LINHA 1: URL DA ROTA + MÉTODO HTTP
        # ==========================================
        layout_linha_url = QHBoxLayout()
        layout_linha_url.setSpacing(12)

        # Bloco URL
        bloco_url = QWidget()
        layout_bloco_url = QVBoxLayout(bloco_url)
        layout_bloco_url.setContentsMargins(0, 0, 0, 0)
        layout_bloco_url.setSpacing(4)

        f_url, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="URL da Rota / Endpoint:",
            titulo_ajuda="URL da Rota / Endpoint",
            texto_ajuda=(
                "Endereço HTTP/HTTPS completo da API ou serviço que você deseja testar "
                "(exemplo: https://httpbin.org/get ou https://api.suaempresa.com/v1/recurso).\n\n"
                "Todas as requisições disparadas pelo teste terão este destino."
            ),
            destaque=True
        )
        self.entry_url = QLineEdit("https://httpbin.org/get")
        self.entry_url.setPlaceholderText("https://api.exemplo.com/endpoint")
        layout_bloco_url.addWidget(f_url)
        layout_bloco_url.addWidget(self.entry_url)
        layout_linha_url.addWidget(bloco_url, stretch=3)

        # Bloco Método HTTP
        bloco_metodo = QWidget()
        layout_bloco_metodo = QVBoxLayout(bloco_metodo)
        layout_bloco_metodo.setContentsMargins(0, 0, 0, 0)
        layout_bloco_metodo.setSpacing(4)

        f_metodo, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Método HTTP:",
            titulo_ajuda="Método HTTP (Verbo)",
            texto_ajuda=(
                "O tipo de operação HTTP a ser executada:\n\n"
                "• GET: Consulta e leitura de dados.\n"
                "• POST: Criação e envio de dados.\n"
                "• PUT / PATCH: Atualização de recursos.\n"
                "• DELETE: Exclusão de recursos.\n"
                "• HEAD / OPTIONS: Verificação de cabeçalhos e métodos."
            )
        )
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        layout_bloco_metodo.addWidget(f_metodo)
        layout_bloco_metodo.addWidget(self.combo_metodo)
        layout_linha_url.addWidget(bloco_metodo, stretch=1)

        layout_principal.addLayout(layout_linha_url)

        # ==========================================
        # LINHA 2: 4 PARÂMETROS NUMÉRICOS ALINHADOS
        # ==========================================
        layout_linha_params = QHBoxLayout()
        layout_linha_params.setSpacing(12)

        # 1. Total de Requisições
        bloco_qtd = QWidget()
        l_qtd = QVBoxLayout(bloco_qtd)
        l_qtd.setContentsMargins(0, 0, 0, 0)
        l_qtd.setSpacing(4)
        f_qtd, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Total Requisições:",
            titulo_ajuda="Total de Requisições",
            texto_ajuda="Quantidade total de requisições disparadas em toda a bateria de teste."
        )
        self.spin_qtd = QSpinBox()
        self.spin_qtd.setRange(1, 100000)
        self.spin_qtd.setValue(50)
        l_qtd.addWidget(f_qtd)
        l_qtd.addWidget(self.spin_qtd)
        layout_linha_params.addWidget(bloco_qtd)

        # 2. Concorrência (Threads)
        bloco_conc = QWidget()
        l_conc = QVBoxLayout(bloco_conc)
        l_conc.setContentsMargins(0, 0, 0, 0)
        l_conc.setSpacing(4)
        f_concorrencia, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Concorrência (Threads):",
            titulo_ajuda="Concorrência (Threads Simultâneas)",
            texto_ajuda=(
                "Número de requisições disparadas simultaneamente em paralelo.\n\n"
                "Em vez de enviar uma requisição por vez em fila única, a aplicação cria múltiplos "
                "trabalhadores paralelos para simular vários usuários acessando a API no mesmo instante exato.\n\n"
                "Exemplo: Concorrência 10 significa 10 requisições simultâneas em paralelo."
            )
        )
        self.spin_concorrencia = QSpinBox()
        self.spin_concorrencia.setRange(1, 200)
        self.spin_concorrencia.setValue(5)
        l_conc.addWidget(f_concorrencia)
        l_conc.addWidget(self.spin_concorrencia)
        layout_linha_params.addWidget(bloco_conc)

        # 3. Delay entre envios
        bloco_delay = QWidget()
        l_delay = QVBoxLayout(bloco_delay)
        l_delay.setContentsMargins(0, 0, 0, 0)
        l_delay.setSpacing(4)
        f_delay, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Delay (ms):",
            titulo_ajuda="Delay / Intervalo entre Envios",
            texto_ajuda=(
                "Pausa em milissegundos aguardada antes de cada envio.\n\n"
                "• 0 ms: Disparo contínuo máximo (teste de estresse / rajada).\n"
                "• > 0 ms: Espaçamento para cadência moderada."
            )
        )
        self.spin_delay = QSpinBox()
        self.spin_delay.setRange(0, 10000)
        self.spin_delay.setValue(0)
        l_delay.addWidget(f_delay)
        l_delay.addWidget(self.spin_delay)
        layout_linha_params.addWidget(bloco_delay)

        # 4. Timeout (s)
        bloco_timeout = QWidget()
        l_timeout = QVBoxLayout(bloco_timeout)
        l_timeout.setContentsMargins(0, 0, 0, 0)
        l_timeout.setSpacing(4)
        f_timeout, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Timeout (s):",
            titulo_ajuda="Timeout (Tempo Limite)",
            texto_ajuda="Tempo limite (em segundos) de espera antes de considerar falha por tempo esgotado."
        )
        self.spin_timeout = QSpinBox()
        self.spin_timeout.setRange(1, 120)
        self.spin_timeout.setValue(10)
        l_timeout.addWidget(f_timeout)
        l_timeout.addWidget(self.spin_timeout)
        layout_linha_params.addWidget(bloco_timeout)

        layout_principal.addLayout(layout_linha_params)

        # ==========================================
        # LINHA 3: CADERNO DE ABAS (HEADERS / BODY)
        # ==========================================
        self.tabs_opcoes = QTabWidget()

        # Aba Headers
        tab_headers = QWidget()
        layout_tab_headers = QVBoxLayout(tab_headers)
        layout_tab_headers.setContentsMargins(8, 6, 8, 6)
        layout_tab_headers.setSpacing(4)

        f_hdr_info, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Formato: Um por linha como 'Chave: Valor' ou objeto JSON.",
            titulo_ajuda="Cabeçalhos HTTP (Headers)",
            texto_ajuda="Exemplos: Authorization: Bearer <token>, Content-Type: application/json."
        )
        layout_tab_headers.addWidget(f_hdr_info)

        self.txt_headers = QTextEdit()
        self.txt_headers.setPlainText("Accept: application/json\nContent-Type: application/json")
        self.txt_headers.setMinimumHeight(55)
        self.txt_headers.setMaximumHeight(75)
        layout_tab_headers.addWidget(self.txt_headers)
        self.tabs_opcoes.addTab(tab_headers, " Cabeçalhos (Headers) ")

        # Aba Body
        tab_body = QWidget()
        layout_tab_body = QVBoxLayout(tab_body)
        layout_tab_body.setContentsMargins(8, 6, 8, 6)
        layout_tab_body.setSpacing(4)

        f_body_info, _, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Conteúdo a ser enviado no payload (POST / PUT / PATCH):",
            titulo_ajuda="Corpo da Requisição (Payload / Body)",
            texto_ajuda="Dados em formato JSON enviados em requisições POST, PUT e PATCH."
        )
        layout_tab_body.addWidget(f_body_info)

        self.txt_body = QTextEdit()
        self.txt_body.setPlaceholderText("{\n  \"chave\": \"valor\"\n}")
        self.txt_body.setMinimumHeight(55)
        self.txt_body.setMaximumHeight(75)
        layout_tab_body.addWidget(self.txt_body)
        self.tabs_opcoes.addTab(tab_body, " Corpo da Requisição (Body) ")

        layout_principal.addWidget(self.tabs_opcoes)

        # ==========================================
        # LINHA 4: BOTÕES DE DISPARO
        # ==========================================
        layout_botoes = QHBoxLayout()
        layout_botoes.setContentsMargins(0, 2, 0, 0)
        layout_botoes.addStretch()

        self.btn_iniciar = QPushButton("▶  Iniciar Teste")
        self.btn_iniciar.setObjectName("btn_iniciar")
        self.btn_iniciar.clicked.connect(self._disparar_inicio)
        layout_botoes.addWidget(self.btn_iniciar)

        self.btn_cancelar = QPushButton("⏹  Interromper")
        self.btn_cancelar.setObjectName("btn_cancelar")
        self.btn_cancelar.setEnabled(False)
        self.btn_cancelar.clicked.connect(self.solicitar_cancelamento.emit)
        layout_botoes.addWidget(self.btn_cancelar)

        layout_principal.addLayout(layout_botoes)

    def _processar_headers(self) -> dict:
        texto = self.txt_headers.toPlainText().strip()
        if not texto:
            return {}

        if texto.startswith("{") and texto.endswith("}"):
            try:
                dados = json.loads(texto)
                if isinstance(dados, dict):
                    return {str(k): str(v) for k, v in dados.items()}
            except Exception:
                pass

        headers = {}
        for linha in texto.splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            if ":" in linha:
                k, v = linha.split(":", 1)
                headers[k.strip()] = v.strip()
        return headers

    def _disparar_inicio(self):
        try:
            url = self.entry_url.text().strip()
            metodo = self.combo_metodo.currentText()
            timeout = float(self.spin_timeout.value())
            total = int(self.spin_qtd.value())
            concorrencia = int(self.spin_concorrencia.value())
            delay = int(self.spin_delay.value())
            cabecalhos = self._processar_headers()
            corpo = self.txt_body.toPlainText().strip() or None

            config = ConfiguracaoRequisicao(
                url=url,
                metodo=metodo,
                cabecalhos=cabecalhos,
                corpo=corpo,
                tempo_limite_segundos=timeout
            )

            plano = PlanoTeste(
                configuracao=config,
                total_requisicoes=total,
                concorrencia=concorrencia,
                intervalo_milissegundos=delay
            )

            self.solicitar_inicio.emit(plano)

        except ValueError as err:
            QMessageBox.warning(self, "Parâmetro Inválido", str(err))
        except Exception as ex:
            QMessageBox.critical(self, "Erro ao Preparar Teste", f"Ocorreu um erro:\n{str(ex)}")

    def definir_estado_execucao(self, em_execucao: bool):
        habilitado = not em_execucao
        self.entry_url.setEnabled(habilitado)
        self.combo_metodo.setEnabled(habilitado)
        self.spin_timeout.setEnabled(habilitado)
        self.spin_qtd.setEnabled(habilitado)
        self.spin_concorrencia.setEnabled(habilitado)
        self.spin_delay.setEnabled(habilitado)
        self.txt_headers.setEnabled(habilitado)
        self.txt_body.setEnabled(habilitado)

        self.btn_iniciar.setEnabled(habilitado)
        self.btn_cancelar.setEnabled(em_execucao)
