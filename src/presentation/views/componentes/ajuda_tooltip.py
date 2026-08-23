import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

class Tooltip:
    """Gerencia a exibição de balões explicativos (tooltips) flutuantes estilizados."""

    def __init__(self, widget: tk.Widget, texto: str, titulo: Optional[str] = None, delay_ms: int = 200):
        self.widget = widget
        self.texto = texto.strip()
        self.titulo = titulo.strip() if titulo else None
        self.delay_ms = delay_ms
        self._janela_tooltip: Optional[tk.Toplevel] = None
        self._timer_id: Optional[str] = None

        self.widget.bind("<Enter>", self._ao_entrar, add="+")
        self.widget.bind("<Leave>", self._ao_sair, add="+")
        self.widget.bind("<ButtonPress>", self._ao_sair, add="+")

    def _ao_entrar(self, event=None):
        self._cancelar_timer()
        self._timer_id = self.widget.after(self.delay_ms, self.mostrar)

    def _ao_sair(self, event=None):
        self._cancelar_timer()
        self.ocultar()

    def _cancelar_timer(self):
        if self._timer_id:
            try:
                self.widget.after_cancel(self._timer_id)
            except Exception:
                pass
            self._timer_id = None

    def mostrar(self):
        if self._janela_tooltip or not self.texto:
            return

        try:
            # Posição na tela do widget pai
            x_widget = self.widget.winfo_rootx()
            y_widget = self.widget.winfo_rooty()
            altura_widget = self.widget.winfo_height()
            largura_widget = self.widget.winfo_width()

            # Cria janela sem bordas de sistema
            self._janela_tooltip = tk.Toplevel(self.widget)
            self._janela_tooltip.wm_overrideredirect(True)
            self._janela_tooltip.attributes("-topmost", True)

            # Container com fundo moderno escuro
            frame_conteudo = tk.Frame(
                self._janela_tooltip,
                background="#0f172a",
                highlightbackground="#38bdf8",
                highlightthickness=1,
                padx=10,
                pady=8
            )
            frame_conteudo.pack(fill="both", expand=True)

            if self.titulo:
                lbl_titulo = tk.Label(
                    frame_conteudo,
                    text=self.titulo,
                    font=("Segoe UI", 9, "bold"),
                    fg="#38bdf8",
                    bg="#0f172a",
                    anchor="w",
                    justify="left"
                )
                lbl_titulo.pack(fill="x", pady=(0, 4))

            lbl_texto = tk.Label(
                frame_conteudo,
                text=self.texto,
                font=("Segoe UI", 9),
                fg="#f8fafc",
                bg="#0f172a",
                wraplength=340,
                justify="left",
                anchor="w"
            )
            lbl_texto.pack(fill="both", expand=True)

            self._janela_tooltip.update_idletasks()
            largura_tip = self._janela_tooltip.winfo_reqwidth()
            altura_tip = self._janela_tooltip.winfo_reqheight()

            # Posiciona ao lado ou logo abaixo do widget
            largura_tela = self.widget.winfo_screenwidth()
            altura_tela = self.widget.winfo_screenheight()

            pos_x = x_widget + largura_widget + 6
            pos_y = y_widget

            # Se ultrapassar borda direita, joga abaixo ou à esquerda
            if pos_x + largura_tip > largura_tela - 10:
                pos_x = max(10, x_widget - largura_tip - 6)
            if pos_y + altura_tip > altura_tela - 40:
                pos_y = max(10, altura_tela - altura_tip - 45)

            self._janela_tooltip.wm_geometry(f"+{int(pos_x)}+{int(pos_y)}")

        except Exception:
            self.ocultar()

    def ocultar(self):
        if self._janela_tooltip:
            try:
                self._janela_tooltip.destroy()
            except Exception:
                pass
            self._janela_tooltip = None


class BotaoAjuda(tk.Label):
    """Botão visual (?) compacto que exibe explicação em tooltip ao passar o mouse ou em diálogo ao clicar."""

    def __init__(self, master, titulo: str, explicacao: str, **kwargs):
        super().__init__(
            master,
            text="(?)",
            font=("Segoe UI", 8, "bold"),
            fg="#0284c7",
            cursor="hand2",
            padx=2,
            pady=0,
            **kwargs
        )
        self.titulo = titulo
        self.explicacao = explicacao

        self._tooltip = Tooltip(self, texto=self.explicacao, titulo=self.titulo, delay_ms=150)

        self.bind("<Enter>", self._ao_hover, add="+")
        self.bind("<Leave>", self._ao_sair, add="+")
        self.bind("<Button-1>", self._ao_clicar)

    def _ao_hover(self, event=None):
        self.config(fg="#0369a1")

    def _ao_sair(self, event=None):
        self.config(fg="#0284c7")

    def _ao_clicar(self, event=None):
        """Ao clicar no botão de ajuda, também disponibiliza uma janela de diálogo explicativa."""
        self._tooltip.ocultar()
        messagebox.showinfo(f"Ajuda: {self.titulo}", f"{self.titulo}\n\n{self.explicacao}")


def criar_rotulo_com_ajuda(
    master,
    texto_rotulo: str,
    titulo_ajuda: str,
    texto_ajuda: str,
    font_rotulo: Optional[tuple] = None,
    **kwargs
) -> tuple[ttk.Frame, ttk.Label, BotaoAjuda]:
    """Cria um frame horizontal contendo um rótulo ttk.Label e um BotaoAjuda (?) lado a lado."""
    frame = ttk.Frame(master)
    
    font_final = font_rotulo or ("Segoe UI", 9)
    lbl = ttk.Label(frame, text=texto_rotulo, font=font_final, **kwargs)
    lbl.pack(side="left", anchor="w")

    btn_ajuda = BotaoAjuda(frame, titulo=titulo_ajuda, explicacao=texto_ajuda)
    btn_ajuda.pack(side="left", padx=(4, 0), anchor="center")

    return frame, lbl, btn_ajuda
