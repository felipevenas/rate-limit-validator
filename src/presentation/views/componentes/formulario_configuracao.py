import tkinter as tk
from tkinter import ttk, messagebox
import json
from typing import Callable, Optional

from ....domain.entities.configuracao_requisicao import ConfiguracaoRequisicao
from ....domain.entities.plano_teste import PlanoTeste
from .ajuda_tooltip import criar_rotulo_com_ajuda

class FormularioConfiguracao(ttk.LabelFrame):
    """Componente visual para entrada de dados e parâmetros de teste."""

    def __init__(self, master, ao_iniciar: Callable[[PlanoTeste], None], ao_cancelar: Callable[[], None], **kwargs):
        super().__init__(master, text="  Configurações do Teste de Rate Limit  ", padding=12, **kwargs)
        self._ao_iniciar = ao_iniciar
        self._ao_cancelar = ao_cancelar

        self._construir_interface()

    def _construir_interface(self):
        self.columnconfigure(1, weight=1)

        # --- Linha 0: URL / Rota ---
        f_url, self.lbl_url, self.btn_ajuda_url = criar_rotulo_com_ajuda(
            self,
            texto_rotulo="URL da Rota / Endpoint:",
            titulo_ajuda="URL da Rota / Endpoint",
            texto_ajuda=(
                "Endereço HTTP/HTTPS completo da API ou serviço que você deseja testar "
                "(exemplo: https://httpbin.org/get ou https://api.suaempresa.com/v1/recurso).\n\n"
                "Todas as requisições do teste serão disparadas para este destino."
            ),
            font_rotulo=("Segoe UI", 9, "bold")
        )
        f_url.grid(row=0, column=0, sticky="w", pady=(2, 4))

        self.var_url = tk.StringVar(value="https://httpbin.org/get")
        self.entry_url = ttk.Entry(self, textvariable=self.var_url, font=("Segoe UI", 9))
        self.entry_url.grid(row=0, column=1, columnspan=3, sticky="ew", pady=(2, 4), padx=(6, 0))

        # --- Linha 1: Método e Timeout ---
        f_metodo, self.lbl_metodo, self.btn_ajuda_metodo = criar_rotulo_com_ajuda(
            self,
            texto_rotulo="Método HTTP:",
            titulo_ajuda="Método HTTP (Verbo)",
            texto_ajuda=(
                "O tipo de operação HTTP a ser executada na API:\n\n"
                "• GET: Consulta/leitura de informações.\n"
                "• POST: Envio de novos dados (criação).\n"
                "• PUT / PATCH: Atualização de recursos existentes.\n"
                "• DELETE: Remoção de recursos.\n"
                "• HEAD / OPTIONS: Verificação de cabeçalhos e métodos permitidos."
            )
        )
        f_metodo.grid(row=1, column=0, sticky="w", pady=4)

        self.var_metodo = tk.StringVar(value="GET")
        self.combo_metodo = ttk.Combobox(
            self,
            textvariable=self.var_metodo,
            values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
            state="readonly",
            width=10
        )
        self.combo_metodo.grid(row=1, column=1, sticky="w", pady=4, padx=(6, 0))

        f_timeout, self.lbl_timeout, self.btn_ajuda_timeout = criar_rotulo_com_ajuda(
            self,
            texto_rotulo="Timeout (segundos):",
            titulo_ajuda="Timeout (Tempo Limite)",
            texto_ajuda=(
                "Tempo máximo (em segundos) que a aplicação aguarda pela resposta do servidor "
                "antes de cancelar a requisição e contabilizar como Falha/Timeout."
            )
        )
        f_timeout.grid(row=1, column=2, sticky="e", pady=4, padx=(12, 6))

        self.var_timeout = tk.StringVar(value="10")
        self.spin_timeout = ttk.Spinbox(self, from_=1, to=120, textvariable=self.var_timeout, width=8)
        self.spin_timeout.grid(row=1, column=3, sticky="w", pady=4)

        # --- Linha 2: Quantidade de Requisições e Concorrência ---
        f_qtd, self.lbl_qtd, self.btn_ajuda_qtd = criar_rotulo_com_ajuda(
            self,
            texto_rotulo="Total de Requisições:",
            titulo_ajuda="Total de Requisições",
            texto_ajuda=(
                "Quantidade total de requisições que serão disparadas ao longo de toda a bateria "
                "de teste para analisar o comportamento e limite de vazão da API."
            )
        )
        f_qtd.grid(row=2, column=0, sticky="w", pady=4)

        self.var_qtd = tk.StringVar(value="50")
        self.spin_qtd = ttk.Spinbox(self, from_=1, to=100000, textvariable=self.var_qtd, width=12)
        self.spin_qtd.grid(row=2, column=1, sticky="w", pady=4, padx=(6, 0))

        f_concorrencia, self.lbl_concorrencia, self.btn_ajuda_concorrencia = criar_rotulo_com_ajuda(
            self,
            texto_rotulo="Concorrência (Threads):",
            titulo_ajuda="Concorrência (Threads Simultâneas)",
            texto_ajuda=(
                "Número de requisições disparadas simultaneamente em paralelo.\n\n"
                "Em vez de enviar uma requisição por vez em fila única, a aplicação cria múltiplos "
                "fluxos de execução independentes (threads de trabalhadores) para simular vários "
                "usuários ou clientes acessando a API no mesmo instante exato.\n\n"
                "Exemplo: Com Concorrência 10, haverá 10 requisições acontecendo ao mesmo tempo no servidor."
            )
        )
        f_concorrencia.grid(row=2, column=2, sticky="e", pady=4, padx=(12, 6))

        self.var_concorrencia = tk.StringVar(value="5")
        self.spin_concorrencia = ttk.Spinbox(self, from_=1, to=200, textvariable=self.var_concorrencia, width=8)
        self.spin_concorrencia.grid(row=2, column=3, sticky="w", pady=4)

        # --- Linha 3: Intervalo / Delay ---
        f_delay, self.lbl_delay, self.btn_ajuda_delay = criar_rotulo_com_ajuda(
            self,
            texto_rotulo="Delay entre envios (ms):",
            titulo_ajuda="Delay / Intervalo entre Envios",
            texto_ajuda=(
                "Tempo de pausa em milissegundos (ms) que cada thread aguarda antes de disparar "
                "a próxima requisição.\n\n"
                "• 0 ms: Envio com velocidade máxima contínua (estresse/rajada).\n"
                "• > 0 ms: Introduz um espaçamento para simular cadência controlada de requisições."
            )
        )
        f_delay.grid(row=3, column=0, sticky="w", pady=4)

        self.var_delay = tk.StringVar(value="0")
        self.spin_delay = ttk.Spinbox(self, from_=0, to=10000, textvariable=self.var_delay, width=12)
        self.spin_delay.grid(row=3, column=1, sticky="w", pady=4, padx=(6, 0))

        # --- Linha 4: Caderno de Abas (Headers e Body) ---
        self.notebook_opcoes = ttk.Notebook(self)
        self.notebook_opcoes.grid(row=4, column=0, columnspan=4, sticky="ew", pady=(10, 6))

        # Aba Cabeçalhos
        frame_headers = ttk.Frame(self.notebook_opcoes, padding=6)
        self.notebook_opcoes.add(frame_headers, text=" Cabeçalhos (Headers) ")

        f_headers_lbl, self.lbl_info_headers, self.btn_ajuda_headers = criar_rotulo_com_ajuda(
            frame_headers,
            texto_rotulo="Formato: Um por linha como 'Chave: Valor' ou JSON.",
            titulo_ajuda="Cabeçalhos HTTP (Headers)",
            texto_ajuda=(
                "Metadados adicionais enviados junto com a requisição.\n\n"
                "Exemplos comuns:\n"
                "• Authorization: Bearer <seu_token_jwt>\n"
                "• Content-Type: application/json\n"
                "• X-API-Key: 123456\n\n"
                "Você pode digitar no formato 'Chave: Valor' (uma por linha) ou colar um objeto JSON."
            ),
            font_rotulo=("Segoe UI", 8, "italic")
        )
        f_headers_lbl.pack(anchor="w", pady=(0, 2))

        self.txt_headers = tk.Text(frame_headers, height=3, font=("Consolas", 9), wrap="none")
        self.txt_headers.insert("1.0", "Accept: application/json\nContent-Type: application/json")
        self.txt_headers.pack(fill="both", expand=True)

        # Aba Corpo (Body JSON)
        frame_body = ttk.Frame(self.notebook_opcoes, padding=6)
        self.notebook_opcoes.add(frame_body, text=" Corpo da Requisição (Body) ")

        f_body_lbl, self.lbl_info_body, self.btn_ajuda_body = criar_rotulo_com_ajuda(
            frame_body,
            texto_rotulo="Conteúdo a ser enviado no payload (POST / PUT / PATCH):",
            titulo_ajuda="Corpo da Requisição (Payload / Body)",
            texto_ajuda=(
                "Os dados enviados no corpo da requisição, geralmente no formato JSON.\n\n"
                "Utilizado principalmente em métodos que criam ou alteram registros no servidor (POST, PUT e PATCH).\n"
                "Exemplo: {\"nome\": \"João\", \"email\": \"joao@exemplo.com\"}"
            ),
            font_rotulo=("Segoe UI", 8, "italic")
        )
        f_body_lbl.pack(anchor="w", pady=(0, 2))

        self.txt_body = tk.Text(frame_body, height=3, font=("Consolas", 9), wrap="none")
        self.txt_body.pack(fill="both", expand=True)

        # --- Linha 5: Botões de Ação ---
        frame_botoes = ttk.Frame(self)
        frame_botoes.grid(row=5, column=0, columnspan=4, sticky="e", pady=(8, 2))

        self.btn_iniciar = ttk.Button(
            frame_botoes,
            text="▶  Iniciar Teste",
            command=self._disparar_inicio
        )
        self.btn_iniciar.pack(side="left", padx=4)

        self.btn_cancelar = ttk.Button(
            frame_botoes,
            text="⏹  Interromper",
            command=self._ao_cancelar,
            state="disabled"
        )
        self.btn_cancelar.pack(side="left", padx=4)

    def _processar_headers(self) -> dict:
        """Converte o texto digitado em dicionário de headers."""
        texto = self.txt_headers.get("1.0", "end").strip()
        if not texto:
            return {}

        # Tenta interpretar como JSON
        if texto.startswith("{") and texto.endswith("}"):
            try:
                dados = json.loads(texto)
                if isinstance(dados, dict):
                    return {str(k): str(v) for k, v in dados.items()}
            except Exception:
                pass

        # Interpreta linha a linha 'Chave: Valor'
        headers = {}
        for linha in texto.splitlines():
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            if ":" in linha:
                chave, valor = linha.split(":", 1)
                headers[chave.strip()] = valor.strip()
        return headers

    def _disparar_inicio(self):
        try:
            url = self.var_url.get().strip()
            metodo = self.var_metodo.get().strip()
            timeout = float(self.var_timeout.get().strip())
            total = int(self.var_qtd.get().strip())
            concorrencia = int(self.var_concorrencia.get().strip())
            delay = int(self.var_delay.get().strip())
            cabecalhos = self._processar_headers()
            corpo = self.txt_body.get("1.0", "end").strip() or None

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

            self._ao_iniciar(plano)

        except ValueError as val_err:
            messagebox.showwarning("Parâmetro Inválido", f"Por favor, verifique os campos informados:\n{str(val_err)}")
        except Exception as ex:
            messagebox.showerror("Erro ao Preparar Teste", f"Ocorreu um erro inesperado:\n{str(ex)}")

    def definir_estado_execucao(self, em_execucao: bool):
        """Habilita ou desabilita os controles durante a execução."""
        estado_inputs = "disabled" if em_execucao else "normal"
        self.entry_url.config(state=estado_inputs)
        self.combo_metodo.config(state="disabled" if em_execucao else "readonly")
        self.spin_timeout.config(state=estado_inputs)
        self.spin_qtd.config(state=estado_inputs)
        self.spin_concorrencia.config(state=estado_inputs)
        self.spin_delay.config(state=estado_inputs)
        self.txt_headers.config(state=estado_inputs)
        self.txt_body.config(state=estado_inputs)

        self.btn_iniciar.config(state="disabled" if em_execucao else "normal")
        self.btn_cancelar.config(state="normal" if em_execucao else "disabled")
