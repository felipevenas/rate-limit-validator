from typing import Optional, List
from PySide6.QtWidgets import (
    QGroupBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

from ....domain.entities.resumo_metricas import ResumoMetricas
from .botao_ajuda_qt import BotaoAjudaQt, criar_rotulo_com_ajuda_qt

class CardMetricaQt(QFrame):
    """Card visual moderno e minimalista para métricas em tempo real."""

    def __init__(self, titulo: str, valor_inicial: str, chave_tipo: str, explicacao: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("card_metrica")
        self.setProperty("metrica_tipo", chave_tipo)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setMinimumWidth(105)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        # Cabeçalho do Card (Indicador de Cor + Título + Botão ?)
        layout_cabecalho = QHBoxLayout()
        layout_cabecalho.setContentsMargins(0, 0, 0, 0)
        layout_cabecalho.setSpacing(4)

        # Ponto colorido semântico
        self.lbl_ponto = QLabel("●")
        self.lbl_ponto.setObjectName("lbl_card_ponto")
        self.lbl_ponto.setProperty("metrica_tipo", chave_tipo)
        layout_cabecalho.addWidget(self.lbl_ponto)

        lbl_tit = QLabel(titulo)
        lbl_tit.setObjectName("lbl_card_titulo")
        layout_cabecalho.addWidget(lbl_tit)
        layout_cabecalho.addStretch()

        btn_ajuda = BotaoAjudaQt(titulo=titulo, explicacao=explicacao)
        layout_cabecalho.addWidget(btn_ajuda)
        layout.addLayout(layout_cabecalho)

        # Valor em Destaque
        self.lbl_valor = QLabel(valor_inicial)
        self.lbl_valor.setObjectName("lbl_card_valor")
        self.lbl_valor.setProperty("metrica_tipo", chave_tipo)
        self.lbl_valor.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_valor)

    def definir_valor(self, texto: str):
        self.lbl_valor.setText(texto)


class PainelMetricasQt(QGroupBox):
    """Painel de Métricas em Tempo Real no PySide6 com suporte a temas dinâmicos."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__("  Métricas em Tempo Real  ", parent)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self._cards: List[CardMetricaQt] = []
        self._construir_interface()

    def _construir_interface(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setSpacing(8)
        layout_principal.setContentsMargins(12, 14, 12, 10)

        # --- Linha de Progresso ---
        f_prog, self.lbl_progresso, _ = criar_rotulo_com_ajuda_qt(
            texto_rotulo="Progresso: 0 / 0 (0.0%)",
            titulo_ajuda="Progresso da Bateria de Testes",
            texto_ajuda=(
                "Indica a quantidade de requisições já processadas em relação ao total planejado "
                "e o percentual concluído em tempo real."
            ),
            destaque=True
        )
        layout_principal.addWidget(f_prog)

        self.barra_progresso = QProgressBar()
        self.barra_progresso.setRange(0, 100)
        self.barra_progresso.setValue(0)
        self.barra_progresso.setTextVisible(False)
        layout_principal.addWidget(self.barra_progresso)

        # --- Grid de Cards Responsivos ---
        layout_cards = QHBoxLayout()
        layout_cards.setSpacing(8)

        # Card 1: Sucesso 2xx
        self.card_sucesso = CardMetricaQt(
            titulo="Sucesso (2xx)",
            valor_inicial="0",
            chave_tipo="sucesso",
            explicacao=(
                "Requisições que foram aceitas e respondidas com sucesso pela API (ex: 200 OK, 201 Created, 204 No Content).\n\n"
                "Indica que a requisição foi processada normalmente sem bloqueios."
            )
        )
        layout_cards.addWidget(self.card_sucesso)
        self._cards.append(self.card_sucesso)

        # Card 2: Rate Limit 429
        self.card_rate_limit = CardMetricaQt(
            titulo="Rate Limit (429)",
            valor_inicial="0",
            chave_tipo="rate_limit",
            explicacao=(
                "Requisições bloqueadas pelo servidor com o código HTTP 429 (Too Many Requests).\n\n"
                "Isso comprova que a política de rate limiting da API entrou em ação para conter o volume de disparos."
            )
        )
        layout_cards.addWidget(self.card_rate_limit)
        self._cards.append(self.card_rate_limit)

        # Card 3: Erros / Falhas
        self.card_erros = CardMetricaQt(
            titulo="Erros / Falhas",
            valor_inicial="0",
            chave_tipo="erro",
            explicacao=(
                "Requisições que resultaram em erros de conexão de rede, timeouts, status 4xx (como 400 Bad Request, 401 Unauthorized, 404 Not Found) "
                "ou status 5xx (500 Internal Server Error, 502/503/504)."
            )
        )
        layout_cards.addWidget(self.card_erros)
        self._cards.append(self.card_erros)

        # Card 4: Latência Média
        self.card_latencia = CardMetricaQt(
            titulo="Latência Média",
            valor_inicial="0.0 ms",
            chave_tipo="latencia",
            explicacao=(
                "Tempo médio em milissegundos (ms) decorrido entre o envio de cada requisição e o recebimento da resposta completa do servidor.\n\n"
                "Permite monitorar se o servidor fica lento sob alta demanda."
            )
        )
        layout_cards.addWidget(self.card_latencia)
        self._cards.append(self.card_latencia)

        # Card 5: RPS
        self.card_rps = CardMetricaQt(
            titulo="Taxa (RPS)",
            valor_inicial="0.0 req/s",
            chave_tipo="rps",
            explicacao=(
                "Mede a vazão efetiva do teste em Requisições por Segundo (Requests Per Second).\n\n"
                "Indica a velocidade real com que as respostas estão sendo processadas."
            )
        )
        layout_cards.addWidget(self.card_rps)
        self._cards.append(self.card_rps)

        layout_principal.addLayout(layout_cards)

    def atualizar_metricas(self, metricas: ResumoMetricas):
        """Atualiza todos os componentes com novos dados estatísticos agregados."""
        self.lbl_progresso.setText(
            f"Progresso: {metricas.total_enviadas} / {metricas.total_esperado} ({metricas.percentual_concluido:.1f}%)"
        )
        self.barra_progresso.setValue(int(metricas.percentual_concluido))

        self.card_sucesso.definir_valor(str(metricas.sucessos_2xx))
        self.card_rate_limit.definir_valor(str(metricas.bloqueios_429))
        self.card_erros.definir_valor(str(metricas.outros_erros))
        self.card_latencia.definir_valor(f"{metricas.latencia_media_ms:.1f} ms")
        self.card_rps.definir_valor(f"{metricas.requisicoes_por_segundo:.1f} req/s")

    def resetar(self, total_esperado: int = 0):
        """Reseta os indicadores para um novo início de teste."""
        self.lbl_progresso.setText(f"Progresso: 0 / {total_esperado} (0.0%)")
        self.barra_progresso.setValue(0)
        self.card_sucesso.definir_valor("0")
        self.card_rate_limit.definir_valor("0")
        self.card_erros.definir_valor("0")
        self.card_latencia.definir_valor("0.0 ms")
        self.card_rps.definir_valor("0.0 req/s")
