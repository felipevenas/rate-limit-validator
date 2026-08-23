import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Callable, Optional
from ....domain.entities.resultado_requisicao import ResultadoRequisicao
from .ajuda_tooltip import BotaoAjuda

class TabelaHistorico(ttk.LabelFrame):
    """Componente visual que lista os disparos individuais de requisições com filtros e exportação."""

    def __init__(self, master, ao_exportar_csv: Callable[[str], None], **kwargs):
        super().__init__(master, text="  Registro Detalhado de Requisições  ", padding=8, **kwargs)
        self._ao_exportar_csv = ao_exportar_csv
        self.var_autoscroll = tk.BooleanVar(value=True)

        self._construir_interface()

    def _construir_interface(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # --- Frame da Tabela com Barras de Rolagem ---
        frame_tabela = ttk.Frame(self)
        frame_tabela.grid(row=0, column=0, sticky="nsew")
        frame_tabela.rowconfigure(0, weight=1)
        frame_tabela.columnconfigure(0, weight=1)

        colunas = ("id", "hora", "status", "situacao", "latencia", "rate_limit", "retry_after", "detalhes")
        self.tree = ttk.Treeview(
            frame_tabela,
            columns=colunas,
            show="headings",
            selectmode="extended"
        )

        # Configurações de Cabeçalho e Larguras
        self.tree.heading("id", text="# ID")
        self.tree.heading("hora", text="Horário")
        self.tree.heading("status", text="Status HTTP")
        self.tree.heading("situacao", text="Situação")
        self.tree.heading("latencia", text="Latência (ms)")
        self.tree.heading("rate_limit", text="Rate Limit?")
        self.tree.heading("retry_after", text="Retry-After")
        self.tree.heading("detalhes", text="Detalhes / Mensagem")

        self.tree.column("id", width=55, anchor="center")
        self.tree.column("hora", width=95, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("situacao", width=120, anchor="center")
        self.tree.column("latencia", width=95, anchor="e")
        self.tree.column("rate_limit", width=90, anchor="center")
        self.tree.column("retry_after", width=100, anchor="center")
        self.tree.column("detalhes", width=260, anchor="w")

        # Tags de cores para destaque de linhas
        self.tree.tag_configure("sucesso", background="#e8f5e9")
        self.tree.tag_configure("rate_limit", background="#ffebee", foreground="#b71c1c")
        self.tree.tag_configure("erro", background="#fff3e0")

        # Scrollbars
        scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # --- Barra Inferior de Ações ---
        frame_acoes = ttk.Frame(self)
        frame_acoes.grid(row=1, column=0, sticky="ew", pady=(6, 0))

        chk_scroll = ttk.Checkbutton(
            frame_acoes,
            text="Rolar automaticamente para o final",
            variable=self.var_autoscroll
        )
        chk_scroll.pack(side="left", padx=4)

        self.btn_ajuda_tabela = BotaoAjuda(
            frame_acoes,
            titulo="Colunas do Registro de Requisições",
            explicacao=(
                "Significado de cada coluna na tabela:\n\n"
                "• # ID: Número sequencial da requisição disparada.\n"
                "• Horário: Momento exato em que a resposta foi recebida.\n"
                "• Status HTTP: Código retornado pelo servidor (ex: 200 OK, 429 Too Many Requests, 500).\n"
                "• Situação: Classificação amigável (Sucesso 2xx, Bloqueado 429, Erro/Falha).\n"
                "• Latência (ms): Tempo total de resposta da requisição em milissegundos.\n"
                "• Rate Limit?: Indica se a requisição sofreu restrição por limite de taxa.\n"
                "• Retry-After: Cabeçalho com tempo de espera recomendado pelo servidor.\n"
                "• Detalhes / Mensagem: Erros de conexão ou corpo resumido da resposta."
            )
        )
        self.btn_ajuda_tabela.pack(side="left", padx=(4, 0))

        self.btn_exportar = ttk.Button(
            frame_acoes,
            text="💾  Exportar Relatório (CSV)",
            command=self._disparar_exportacao
        )
        self.btn_exportar.pack(side="right", padx=4)

        btn_limpar = ttk.Button(
            frame_acoes,
            text="🗑  Limpar Tabela",
            command=self.limpar
        )
        btn_limpar.pack(side="right", padx=4)

    def adicionar_resultado(self, resultado: ResultadoRequisicao):
        """Insere uma nova linha na tabela formatada."""
        hora_str = resultado.data_hora.strftime("%H:%M:%S.%f")[:-3]
        status_str = str(resultado.codigo_status) if resultado.codigo_status > 0 else "Falha"

        if resultado.foi_rate_limit:
            situacao = "Bloqueado (429)"
            tag = "rate_limit"
            rl_str = "SIM (429)"
        elif 200 <= resultado.codigo_status <= 299:
            situacao = "Sucesso (2xx)"
            tag = "sucesso"
            rl_str = "NÃO"
        else:
            situacao = "Erro/Falha"
            tag = "erro"
            rl_str = "NÃO"

        detalhe = resultado.mensagem_erro or resultado.mensagem_status

        item_id = self.tree.insert(
            "",
            "end",
            values=(
                f"#{resultado.id_requisicao}",
                hora_str,
                status_str,
                situacao,
                f"{resultado.latencia_ms:.1f}",
                rl_str,
                resultado.tempo_espera_retry_after or "-",
                detalhe
            ),
            tags=(tag,)
        )

        if self.var_autoscroll.get():
            self.tree.see(item_id)

    def limpar(self):
        """Remove todas as linhas da tabela."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def _disparar_exportacao(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar Relatório de Teste de Rate Limit",
            defaultextension=".csv",
            filetypes=[("Arquivo CSV (*.csv)", "*.csv"), ("Todos os Arquivos (*.*)", "*.*")]
        )
        if caminho:
            try:
                self._ao_exportar_csv(caminho)
                messagebox.showinfo("Exportação Concluída", f"Relatório salvo com sucesso em:\n{caminho}")
            except Exception as ex:
                messagebox.showerror("Erro na Exportação", f"Não foi possível salvar o arquivo:\n{str(ex)}")
