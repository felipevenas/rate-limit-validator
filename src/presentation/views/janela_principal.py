import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from .componentes.formulario_configuracao import FormularioConfiguracao
from .componentes.painel_metricas import PainelMetricas
from .componentes.tabela_historico import TabelaHistorico
from ..controllers.controlador_principal import ControladorPrincipal
from ...domain.entities.plano_teste import PlanoTeste
from ...domain.entities.resultado_requisicao import ResultadoRequisicao
from ...domain.entities.resumo_metricas import ResumoMetricas

class JanelaPrincipal(tk.Tk):
    """Janela Mestre da Aplicação de Testes de Rate Limit."""

    def __init__(self, controlador: ControladorPrincipal):
        super().__init__()
        self.controlador = controlador

        self.title("Validador de Rate Limit - Testador de APIs")
        self.geometry("980x740")
        self.minsize(820, 580)

        self._configurar_estilos()
        self._construir_interface()

        # Inicia o loop de verificação da fila thread-safe
        self.after(50, self._processar_fila_periodica)

        # Encerramento gracioso ao fechar a janela
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar_janela)

    def _configurar_estilos(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        fonte_padrao = ("Segoe UI", 9)
        fonte_titulo = ("Segoe UI", 10, "bold")

        style.configure(".", font=fonte_padrao)
        style.configure("TLabelframe.Label", font=fonte_titulo, foreground="#1e293b")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", rowheight=24)

    def _construir_interface(self):
        # Container principal com padding
        conteiner = ttk.Frame(self, padding=10)
        conteiner.pack(fill="both", expand=True)

        conteiner.columnconfigure(0, weight=1)
        conteiner.rowconfigure(2, weight=1)

        # 1. Formulário de Configuração
        self.form_config = FormularioConfiguracao(
            conteiner,
            ao_iniciar=self._iniciar_teste,
            ao_cancelar=self._cancelar_teste
        )
        self.form_config.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        # 2. Painel de Métricas em Destaque
        self.painel_metricas = PainelMetricas(conteiner)
        self.painel_metricas.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        # 3. Tabela de Histórico e Registro de Disparos
        self.tabela_historico = TabelaHistorico(
            conteiner,
            ao_exportar_csv=self._exportar_csv
        )
        self.tabela_historico.grid(row=2, column=0, sticky="nsew")

        # 4. Barra de Status no Rodapé
        self.frame_status = ttk.Frame(self, relief="sunken", padding=(8, 4))
        self.frame_status.pack(side="bottom", fill="x")

        self.lbl_status = ttk.Label(
            self.frame_status,
            text="Status: Pronto para iniciar teste.",
            font=("Segoe UI", 8)
        )
        self.lbl_status.pack(side="left")

        self.lbl_versao = ttk.Label(
            self.frame_status,
            text="Versão 1.0.0 (Português - BR)",
            font=("Segoe UI", 8, "italic")
        )
        self.lbl_versao.pack(side="right")

    def _iniciar_teste(self, plano: PlanoTeste):
        """Callback acionado pelo botão Iniciar."""
        self.painel_metricas.resetar(total_esperado=plano.total_requisicoes)
        self.tabela_historico.limpar()
        self.form_config.definir_estado_execucao(em_execucao=True)
        self.lbl_status.config(
            text=f"Status: Executando bateria de {plano.total_requisicoes} requisições com concorrência {plano.concorrencia}..."
        )

        self.controlador.iniciar_teste(
            plano=plano,
            ao_atualizar=self._ao_receber_item,
            ao_finalizar=self._ao_finalizar_teste
        )

    def _cancelar_teste(self):
        """Callback acionado pelo botão Interromper."""
        self.lbl_status.config(text="Status: Solicitando interrupção do teste...")
        self.controlador.cancelar_teste()

    def _ao_receber_item(self, resultado: ResultadoRequisicao, metricas: ResumoMetricas):
        """Atualização visual de cada requisição individual."""
        self.painel_metricas.atualizar_metricas(metricas)
        self.tabela_historico.adicionar_resultado(resultado)

    def _ao_finalizar_teste(self, metricas: ResumoMetricas, cancelado: bool):
        """Callback acionado quando o teste termina ou é cancelado."""
        self.form_config.definir_estado_execucao(em_execucao=False)
        self.painel_metricas.atualizar_metricas(metricas)

        if cancelado:
            self.lbl_status.config(
                text=f"Status: Teste cancelado pelo usuário! Processadas {metricas.total_enviadas} de {metricas.total_esperado} requisições."
            )
            messagebox.showwarning(
                "Teste Interrompido",
                f"A execução foi interrompida antes do final.\nTotal processado: {metricas.total_enviadas} requisições."
            )
        else:
            self.lbl_status.config(
                text=f"Status: Teste concluído com sucesso! {metricas.total_enviadas} requisições em {metricas.tempo_total_segundos:.2f}s ({metricas.requisicoes_por_segundo:.1f} req/s)."
            )
            msg_resultado = (
                f"Bateria de testes finalizada!\n\n"
                f"• Total Enviadas: {metricas.total_enviadas}\n"
                f"• Sucessos (2xx): {metricas.sucessos_2xx}\n"
                f"• Rate Limit (429): {metricas.bloqueios_429}\n"
                f"• Erros/Falhas: {metricas.outros_erros}\n"
                f"• Latência Média: {metricas.latencia_media_ms:.1f} ms\n"
                f"• Taxa Efetiva: {metricas.requisicoes_por_segundo:.1f} req/s"
            )
            messagebox.showinfo("Bateria Concluída", msg_resultado)

    def _processar_fila_periodica(self):
        """Drena periodicamente a fila de eventos do controlador na thread da UI."""
        self.controlador.processar_eventos_fila(
            callback_item=self._ao_receber_item,
            callback_fim=self._ao_finalizar_teste,
            callback_erro=lambda err: messagebox.showerror("Erro de Execução", f"Erro no teste:\n{err}")
        )
        self.after(50, self._processar_fila_periodica)

    def _exportar_csv(self, caminho: str):
        self.controlador.exportar_para_csv(caminho)

    def _ao_fechar_janela(self):
        if self.controlador.em_execucao:
            resposta = messagebox.askyesno(
                "Teste em Execução",
                "Existe um teste de requisições em andamento. Deseja realmente interromper e fechar o aplicativo?"
            )
            if not resposta:
                return
            self.controlador.cancelar_teste()
        self.destroy()
