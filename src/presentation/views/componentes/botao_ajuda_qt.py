from PySide6.QtWidgets import QPushButton, QMessageBox, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor

class BotaoAjudaQt(QPushButton):
    """Botão visual (?) minimalista com suporte a Tooltip rica em HTML e Diálogo explicativo."""

    def __init__(self, titulo: str, explicacao: str, parent: QWidget = None):
        super().__init__("?", parent)
        self.titulo = titulo
        self.explicacao = explicacao
        self.setObjectName("btn_ajuda")

        self.setFixedSize(18, 18)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        explicacao_html = self.explicacao.replace("\n", "<br>")
        self.setToolTip(
            f"<div style='line-height: 1.4; padding: 2px;'>"
            f"<b>{self.titulo}</b><br><br>"
            f"<span>{explicacao_html}</span>"
            f"</div>"
        )

        self.clicked.connect(self._ao_clicar)

    def _ao_clicar(self):
        msg = QMessageBox(self.window())
        msg.setWindowTitle(f"Ajuda: {self.titulo}")
        msg.setText(f"<h3>{self.titulo}</h3>")
        msg.setInformativeText(self.explicacao)
        msg.setIcon(QMessageBox.Information)
        msg.exec()


def criar_rotulo_com_ajuda_qt(
    texto_rotulo: str,
    titulo_ajuda: str,
    texto_ajuda: str,
    destaque: bool = False
) -> tuple[QWidget, QLabel, BotaoAjudaQt]:
    """Cria um container horizontal compacto com o QLabel e o BotaoAjudaQt perfeitamente alinhados."""
    conteiner = QWidget()
    conteiner.setObjectName("container_rotulo_ajuda")
    layout = QHBoxLayout(conteiner)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(5)

    lbl = QLabel(texto_rotulo)
    if destaque:
        lbl.setObjectName("lbl_destaque")
    else:
        lbl.setObjectName("lbl_parametro")

    btn_ajuda = BotaoAjudaQt(titulo=titulo_ajuda, explicacao=texto_ajuda)

    layout.addWidget(lbl)
    layout.addWidget(btn_ajuda)
    layout.addStretch()

    return conteiner, lbl, btn_ajuda
