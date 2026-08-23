from typing import Optional, Callable
from PySide6.QtWidgets import (
    QGroupBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QCheckBox, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QBrush, QFont

from ....domain.entities.resultado_requisicao import ResultadoRequisicao
from .botao_ajuda_qt import BotaoAjudaQt

class TabelaHistoricoQt(QGroupBox):
    """Componente visual rico de tabela de requisições com ordenação, filtros e suporte a temas."""

    def __init__(self, ao_exportar_csv: Callable[[str], None], parent: Optional[QWidget] = None):
        super().__init__("  Registro Detalhado de Requisições  ", parent)
        self._ao_exportar_csv = ao_exportar_csv
        self._todos_resultados: list[ResultadoRequisicao] = []
        self._modo_escuro = True

        self._construir_interface()

    def _construir_interface(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(8)
        layout_principal.setContentsMargins(12, 14, 12, 10)

        # --- Barra Superior: Busca e Filtros Rápidos ---
        layout_filtros = QHBoxLayout()
        layout_filtros.setSpacing(10)

        lbl_busca = QLabel("Buscar:")
        lbl_busca.setObjectName("lbl_icone_busca")
        self.entry_busca = QLineEdit()
        self.entry_busca.setPlaceholderText("Filtrar por ID, Status, Detalhes...")
        self.entry_busca.textChanged.connect(self._aplicar_filtros)
        layout_filtros.addWidget(lbl_busca)
        layout_filtros.addWidget(self.entry_busca, stretch=2)

        lbl_tipo = QLabel("Filtro:")
        lbl_tipo.setObjectName("lbl_filtro_titulo")
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems(["Todos", "Apenas Sucessos (2xx)", "Apenas Rate Limit (429)", "Apenas Erros/Falhas"])
        self.combo_filtro.currentIndexChanged.connect(self._aplicar_filtros)
        layout_filtros.addWidget(lbl_tipo)
        layout_filtros.addWidget(self.combo_filtro, stretch=1)

        self.chk_autoscroll = QCheckBox("Rolar ao final")
        self.chk_autoscroll.setChecked(True)
        layout_filtros.addWidget(self.chk_autoscroll)

        layout_principal.addLayout(layout_filtros)

        # --- QTableWidget ---
        self.tabela = QTableWidget(0, 8)
        self.tabela.setHorizontalHeaderLabels([
            "# ID", "Horário", "Status HTTP", "Situação",
            "Latência (ms)", "Rate Limit?", "Retry-After", "Detalhes / Mensagem"
        ])
        
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabela.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.horizontalHeader().setStretchLastSection(True)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        # Ordenação manual sob demanda sem travar inserções
        self.tabela.horizontalHeader().sectionClicked.connect(self._ao_clicar_cabecalho)

        # Ajuste de larguras iniciais
        self.tabela.setColumnWidth(0, 60)
        self.tabela.setColumnWidth(1, 95)
        self.tabela.setColumnWidth(2, 95)
        self.tabela.setColumnWidth(3, 130)
        self.tabela.setColumnWidth(4, 100)
        self.tabela.setColumnWidth(5, 95)
        self.tabela.setColumnWidth(6, 95)

        layout_principal.addWidget(self.tabela)

        # --- Barra Inferior de Ações ---
        layout_acoes = QHBoxLayout()
        layout_acoes.setSpacing(8)

        self.btn_ajuda_tabela = BotaoAjudaQt(
            titulo="Colunas do Registro de Requisições",
            explicacao=(
                "Significado de cada coluna na tabela:\n\n"
                "• # ID: Número sequencial da requisição disparada.\n"
                "• Horário: Momento exato em que a resposta foi recebida.\n"
                "• Status HTTP: Código retornado pelo servidor (ex: 200 OK, 429 Too Many Requests, 500).\n"
                "• Situação: Classificação semântica (Sucesso 2xx, Bloqueado 429, Erro/Falha).\n"
                "• Latência (ms): Tempo total de resposta da requisição em milissegundos.\n"
                "• Rate Limit?: Destaca se a requisição sofreu bloqueio de taxa.\n"
                "• Retry-After: Cabeçalho com tempo de espera sugerido pela API.\n"
                "• Detalhes / Mensagem: Erros de conexão ou dados resumidos da resposta."
            )
        )
        layout_acoes.addWidget(self.btn_ajuda_tabela)

        self.lbl_contagem = QLabel("Registros: 0")
        self.lbl_contagem.setObjectName("lbl_contagem_tabela")
        layout_acoes.addWidget(self.lbl_contagem)

        layout_acoes.addStretch()

        self.btn_exportar = QPushButton("Exportar Relatório (CSV)")
        self.btn_exportar.clicked.connect(self._disparar_exportacao)
        layout_acoes.addWidget(self.btn_exportar)

        self.btn_limpar = QPushButton("Limpar")
        self.btn_limpar.clicked.connect(self.limpar)
        layout_acoes.addWidget(self.btn_limpar)

        layout_principal.addLayout(layout_acoes)

    def definir_modo_escuro(self, modo_escuro: bool):
        """Atualiza a paleta de cores das células existentes para o tema selecionado."""
        self._modo_escuro = modo_escuro
        for linha, res in enumerate(self._todos_resultados):
            if linha < self.tabela.rowCount():
                cor_fundo, cor_texto = self._obter_cores_status(res)
                item_status = self.tabela.item(linha, 2)
                item_sit = self.tabela.item(linha, 3)
                if item_status and item_sit:
                    item_status.setBackground(QBrush(cor_fundo))
                    item_status.setForeground(QBrush(cor_texto))
                    item_sit.setBackground(QBrush(cor_fundo))
                    item_sit.setForeground(QBrush(cor_texto))

    def _obter_cores_status(self, resultado: ResultadoRequisicao) -> tuple[QColor, QColor]:
        if self._modo_escuro:
            if resultado.foi_rate_limit:
                return QColor("#2e0b12"), QColor("#fb7185")
            elif 200 <= resultado.codigo_status <= 299:
                return QColor("#062817"), QColor("#4ade80")
            else:
                return QColor("#2e1507"), QColor("#fdba74")
        else:
            if resultado.foi_rate_limit:
                return QColor("#fee2e2"), QColor("#b91c1c")
            elif 200 <= resultado.codigo_status <= 299:
                return QColor("#dcfce7"), QColor("#15803d")
            else:
                return QColor("#ffedd5"), QColor("#c2410c")

    def adicionar_resultado(self, resultado: ResultadoRequisicao):
        """Insere uma nova linha na tabela em tempo real com badges semânticas."""
        self._todos_resultados.append(resultado)
        
        linha = self.tabela.rowCount()
        self.tabela.insertRow(linha)

        hora_str = resultado.data_hora.strftime("%H:%M:%S.%f")[:-3]
        status_str = str(resultado.codigo_status) if resultado.codigo_status > 0 else "Falha"

        if resultado.foi_rate_limit:
            situacao = "Bloqueado (429)"
            rl_str = "SIM (429)"
        elif 200 <= resultado.codigo_status <= 299:
            situacao = "Sucesso (2xx)"
            rl_str = "NÃO"
        else:
            situacao = "Erro/Falha"
            rl_str = "NÃO"

        cor_fundo, cor_texto = self._obter_cores_status(resultado)
        detalhe = resultado.mensagem_erro or resultado.mensagem_status

        # Itens das células
        item_id = QTableWidgetItem(f"#{resultado.id_requisicao}")
        item_id.setTextAlignment(Qt.AlignCenter)

        item_hora = QTableWidgetItem(hora_str)
        item_hora.setTextAlignment(Qt.AlignCenter)

        item_status = QTableWidgetItem(status_str)
        item_status.setTextAlignment(Qt.AlignCenter)
        item_status.setBackground(QBrush(cor_fundo))
        item_status.setForeground(QBrush(cor_texto))
        fonte_status = item_status.font()
        fonte_status.setBold(True)
        item_status.setFont(fonte_status)

        item_sit = QTableWidgetItem(situacao)
        item_sit.setTextAlignment(Qt.AlignCenter)
        item_sit.setBackground(QBrush(cor_fundo))
        item_sit.setForeground(QBrush(cor_texto))

        item_lat = QTableWidgetItem(f"{resultado.latencia_ms:.1f}")
        item_lat.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

        item_rl = QTableWidgetItem(rl_str)
        item_rl.setTextAlignment(Qt.AlignCenter)

        item_retry = QTableWidgetItem(resultado.tempo_espera_retry_after or "-")
        item_retry.setTextAlignment(Qt.AlignCenter)

        item_det = QTableWidgetItem(detalhe)

        self.tabela.setItem(linha, 0, item_id)
        self.tabela.setItem(linha, 1, item_hora)
        self.tabela.setItem(linha, 2, item_status)
        self.tabela.setItem(linha, 3, item_sit)
        self.tabela.setItem(linha, 4, item_lat)
        self.tabela.setItem(linha, 5, item_rl)
        self.tabela.setItem(linha, 6, item_retry)
        self.tabela.setItem(linha, 7, item_det)

        self.lbl_contagem.setText(f"Registros: {len(self._todos_resultados)}")

        self._verificar_visibilidade_linha(linha, resultado)

        if self.chk_autoscroll.isChecked():
            self.tabela.scrollToBottom()

    def _ao_clicar_cabecalho(self, indice_coluna: int):
        """Aplica ordenação pontual ao clicar no cabeçalho."""
        ordem_atual = self.tabela.horizontalHeader().sortIndicatorOrder()
        self.tabela.sortItems(indice_coluna, ordem_atual)

    def _verificar_visibilidade_linha(self, linha: int, resultado: ResultadoRequisicao):
        filtro_tipo = self.combo_filtro.currentText()
        busca = self.entry_busca.text().lower().strip()

        visivel = True

        # Filtro de tipo
        if filtro_tipo == "Apenas Sucessos (2xx)" and not (200 <= resultado.codigo_status <= 299):
            visivel = False
        elif filtro_tipo == "Apenas Rate Limit (429)" and not resultado.foi_rate_limit:
            visivel = False
        elif filtro_tipo == "Apenas Erros/Falhas" and (200 <= resultado.codigo_status <= 299 or resultado.foi_rate_limit):
            visivel = False

        # Filtro textual
        if visivel and busca:
            texto_linha = f"{resultado.id_requisicao} {resultado.codigo_status} {resultado.mensagem_erro or ''} {resultado.mensagem_status}".lower()
            if busca not in texto_linha:
                visivel = False

        self.tabela.setRowHidden(linha, not visivel)

    def _aplicar_filtros(self):
        for linha, res in enumerate(self._todos_resultados):
            if linha < self.tabela.rowCount():
                self._verificar_visibilidade_linha(linha, res)

    def limpar(self):
        """Limpa a tabela e o histórico de forma segura."""
        self._todos_resultados.clear()
        self.tabela.setRowCount(0)
        self.lbl_contagem.setText("Registros: 0")

    def _disparar_exportacao(self):
        caminho, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Relatório de Rate Limit",
            "relatorio_rate_limit.csv",
            "Arquivo CSV (*.csv);;Todos os Arquivos (*)"
        )
        if caminho:
            try:
                self._ao_exportar_csv(caminho)
                QMessageBox.information(
                    self,
                    "Exportação Concluída",
                    f"Relatório exportado com sucesso em:\n{caminho}"
                )
            except Exception as ex:
                QMessageBox.critical(self, "Erro na Exportação", f"Não foi possível salvar o arquivo:\n{str(ex)}")
