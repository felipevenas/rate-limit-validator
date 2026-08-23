import tkinter as tk
from tkinter import ttk
from ....domain.entities.resumo_metricas import ResumoMetricas
from .ajuda_tooltip import BotaoAjuda, criar_rotulo_com_ajuda

class PainelMetricas(ttk.LabelFrame):
    """Componente visual para exibição das métricas e contadores em tempo real."""

    def __init__(self, master, **kwargs):
        super().__init__(master, text="  Métricas em Tempo Real  ", padding=10, **kwargs)
        self._construir_interface()

    def _construir_interface(self):
        self.columnconfigure((0, 1, 2, 3, 4), weight=1)

        # --- Barra de Progresso Superior ---
        frame_progresso = ttk.Frame(self)
        frame_progresso.grid(row=0, column=0, columnspan=5, sticky="ew", pady=(0, 10))
        frame_progresso.columnconfigure(0, weight=1)

        f_prog_header, self.lbl_progresso, self.btn_ajuda_progresso = criar_rotulo_com_ajuda(
            frame_progresso,
            texto_rotulo="Progresso: 0 / 0 (0.0%)",
            titulo_ajuda="Progresso da Bateria de Testes",
            texto_ajuda=(
                "Indica a quantidade de requisições já processadas em relação ao total planejado "
                "e o percentual concluído em tempo real."
            ),
            font_rotulo=("Segoe UI", 9, "bold")
        )
        f_prog_header.grid(row=0, column=0, sticky="w", pady=(0, 2))

        self.barra_progresso = ttk.Progressbar(frame_progresso, mode="determinate", maximum=100)
        self.barra_progresso.grid(row=1, column=0, sticky="ew")

        # --- Cards de Métricas ---
        # Card 1: Sucesso 2xx
        self.card_sucesso = self._criar_card(
            coluna=0,
            titulo="Sucesso (2xx)",
            valor_inicial="0",
            cor_destaque="#2e7d32",
            explicacao=(
                "Requisições que foram aceitas e respondidas com sucesso pela API (ex: 200 OK, 201 Created, 204 No Content).\n\n"
                "Indica que a requisição foi processada normalmente sem bloqueios."
            )
        )

        # Card 2: Rate Limit 429
        self.card_rate_limit = self._criar_card(
            coluna=1,
            titulo="Rate Limit (429)",
            valor_inicial="0",
            cor_destaque="#c62828",
            explicacao=(
                "Requisições bloqueadas pelo servidor com o código HTTP 429 (Too Many Requests).\n\n"
                "Isso comprova que a política de rate limiting da API entrou em ação para conter o volume de disparos."
            )
        )

        # Card 3: Outros Erros
        self.card_erros = self._criar_card(
            coluna=2,
            titulo="Erros / Falhas",
            valor_inicial="0",
            cor_destaque="#e65100",
            explicacao=(
                "Requisições que resultaram em erros de conexão de rede, timeouts, status 4xx (como 400 Bad Request, 401 Unauthorized, 404 Not Found) "
                "ou status 5xx (500 Internal Server Error, 502/503/504)."
            )
        )

        # Card 4: Latência Média
        self.card_latencia = self._criar_card(
            coluna=3,
            titulo="Latência Média",
            valor_inicial="0.0 ms",
            cor_destaque="#1565c0",
            explicacao=(
                "Tempo médio em milissegundos (ms) decorrido entre o envio de cada requisição e o recebimento da resposta completa do servidor.\n\n"
                "Permite monitorar se o servidor fica lento sob alta demanda."
            )
        )

        # Card 5: RPS
        self.card_rps = self._criar_card(
            coluna=4,
            titulo="Taxa (RPS)",
            valor_inicial="0.0 req/s",
            cor_destaque="#4527a0",
            explicacao=(
                "Mede a vazão efetiva do teste em Requisições por Segundo (Requests Per Second).\n\n"
                "Indica a velocidade real com que as respostas estão sendo processadas."
            )
        )

    def _criar_card(self, coluna: int, titulo: str, valor_inicial: str, cor_destaque: str, explicacao: str) -> tk.Label:
        frame_card = ttk.Frame(self, relief="solid", borderwidth=1, padding=6)
        frame_card.grid(row=1, column=coluna, sticky="nsew", padx=3)

        frame_tit = ttk.Frame(frame_card)
        frame_tit.pack(fill="x", pady=(0, 2))

        lbl_tit = ttk.Label(
            frame_tit,
            text=titulo,
            font=("Segoe UI", 8, "bold"),
            anchor="center"
        )
        lbl_tit.pack(side="left", expand=True)

        btn_ajuda = BotaoAjuda(frame_tit, titulo=titulo, explicacao=explicacao)
        btn_ajuda.pack(side="right", padx=(2, 0))

        lbl_val = tk.Label(
            frame_card,
            text=valor_inicial,
            font=("Segoe UI", 13, "bold"),
            fg=cor_destaque,
            anchor="center"
        )
        lbl_val.pack(fill="x")
        return lbl_val

    def atualizar_metricas(self, metricas: ResumoMetricas):
        """Atualiza todos os indicadores visuais do painel com os dados agregados."""
        self.lbl_progresso.config(
            text=f"Progresso: {metricas.total_enviadas} / {metricas.total_esperado} ({metricas.percentual_concluido:.1f}%)"
        )
        self.barra_progresso["value"] = metricas.percentual_concluido

        self.card_sucesso.config(text=str(metricas.sucessos_2xx))
        self.card_rate_limit.config(text=str(metricas.bloqueios_429))
        self.card_erros.config(text=str(metricas.outros_erros))
        self.card_latencia.config(text=f"{metricas.latencia_media_ms:.1f} ms")
        self.card_rps.config(text=f"{metricas.requisicoes_por_segundo:.1f} req/s")

    def resetar(self, total_esperado: int = 0):
        """Reinicia os indicadores para o início de um novo teste."""
        self.lbl_progresso.config(text=f"Progresso: 0 / {total_esperado} (0.0%)")
        self.barra_progresso["value"] = 0
        self.card_sucesso.config(text="0")
        self.card_rate_limit.config(text="0")
        self.card_erros.config(text="0")
        self.card_latencia.config(text="0.0 ms")
        self.card_rps.config(text="0.0 req/s")
