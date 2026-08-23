import time
import urllib.request
import urllib.error
import ssl
from typing import Dict

from ...domain.entities.configuracao_requisicao import ConfiguracaoRequisicao
from ...domain.entities.resultado_requisicao import ResultadoRequisicao
from ...domain.interfaces.cliente_http import IClienteHttp

class ClienteHttpUrllib(IClienteHttp):
    """
    Implementação leve de IClienteHttp usando a biblioteca padrão urllib.
    Não requer pacotes externos e suporta SSL, headers customizados, timeouts e medição precisa de latência.
    """

    def __init__(self, ignorar_verificacao_ssl: bool = False):
        self._contexto_ssl = ssl.create_default_context()
        if ignorar_verificacao_ssl:
            self._contexto_ssl.check_hostname = False
            self._contexto_ssl.verify_mode = ssl.CERT_NONE

    def enviar(self, config: ConfiguracaoRequisicao, id_requisicao: int) -> ResultadoRequisicao:
        # Prepara payload em bytes se houver
        dados_corpo = None
        if config.corpo and config.metodo in {"POST", "PUT", "PATCH", "DELETE"}:
            dados_corpo = config.corpo.encode("utf-8")

        # Configura cabeçalhos padrão se não fornecidos
        headers = dict(config.cabecalhos)
        if "User-Agent" not in headers and "user-agent" not in headers:
            headers["User-Agent"] = "ValidadorRateLimit/1.0 (Python Desktop)"

        requisicao = urllib.request.Request(
            url=config.url,
            data=dados_corpo,
            headers=headers,
            method=config.metodo
        )

        inicio = time.perf_counter()
        try:
            with urllib.request.urlopen(
                requisicao,
                timeout=config.tempo_limite_segundos,
                context=self._contexto_ssl
            ) as resposta:
                fim = time.perf_counter()
                latencia_ms = (fim - inicio) * 1000.0

                headers_resposta: Dict[str, str] = {
                    chave: valor for chave, valor in resposta.headers.items()
                }

                return ResultadoRequisicao.criar_com_sucesso(
                    id_req=id_requisicao,
                    status_code=resposta.status,
                    latencia_ms=latencia_ms,
                    headers=headers_resposta,
                    motivo_status=resposta.reason or f"HTTP {resposta.status}"
                )

        except urllib.error.HTTPError as http_err:
            fim = time.perf_counter()
            latencia_ms = (fim - inicio) * 1000.0

            headers_resposta = {
                chave: valor for chave, valor in http_err.headers.items()
            } if http_err.headers else {}

            return ResultadoRequisicao.criar_com_sucesso(
                id_req=id_requisicao,
                status_code=http_err.code,
                latencia_ms=latencia_ms,
                headers=headers_resposta,
                motivo_status=http_err.reason or f"HTTP {http_err.code}"
            )

        except urllib.error.URLError as url_err:
            fim = time.perf_counter()
            latencia_ms = (fim - inicio) * 1000.0
            motivo = str(url_err.reason)
            return ResultadoRequisicao.criar_com_falha(
                id_req=id_requisicao,
                latencia_ms=latencia_ms,
                erro=f"Erro de URL / Rede: {motivo}"
            )

        except TimeoutError:
            fim = time.perf_counter()
            latencia_ms = (fim - inicio) * 1000.0
            return ResultadoRequisicao.criar_com_falha(
                id_req=id_requisicao,
                latencia_ms=latencia_ms,
                erro=f"Tempo limite excedido ({config.tempo_limite_segundos}s)"
            )

        except Exception as ex:
            fim = time.perf_counter()
            latencia_ms = (fim - inicio) * 1000.0
            return ResultadoRequisicao.criar_com_falha(
                id_req=id_requisicao,
                latencia_ms=latencia_ms,
                erro=f"Erro inesperado: {str(ex)}"
            )
