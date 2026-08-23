from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

@dataclass(frozen=True)
class ResultadoRequisicao:
    """Representa o resultado individual de um disparo de requisição."""
    id_requisicao: int
    data_hora: datetime
    codigo_status: int
    latencia_ms: float
    foi_rate_limit: bool
    tempo_espera_retry_after: Optional[str] = None
    limite_declarado: Optional[str] = None
    limite_restante: Optional[str] = None
    limite_reset: Optional[str] = None
    cabecalhos_resposta: Dict[str, str] = field(default_factory=dict)
    mensagem_status: str = ""
    mensagem_erro: Optional[str] = None

    @classmethod
    def criar_com_sucesso(
        cls,
        id_req: int,
        status_code: int,
        latencia_ms: float,
        headers: Dict[str, str],
        motivo_status: str = ""
    ) -> "ResultadoRequisicao":
        """Fabrica um resultado a partir de uma resposta HTTP recebida."""
        # Normaliza chaves de headers para caixa baixa para busca rápida
        headers_lower = {k.lower(): v for k, v in headers.items()}

        # 429 é o padrão RFC 6585 para Rate Limit / Too Many Requests
        # Algumas APIs legadas usam 403 / 503 com mensagens específicas
        eh_429 = status_code == 429

        retry_after = (
            headers_lower.get("retry-after")
            or headers_lower.get("x-ratelimit-reset-after")
            or headers_lower.get("ratelimit-reset")
        )
        limite = (
            headers_lower.get("x-ratelimit-limit")
            or headers_lower.get("ratelimit-limit")
        )
        restante = (
            headers_lower.get("x-ratelimit-remaining")
            or headers_lower.get("ratelimit-remaining")
        )
        reset = (
            headers_lower.get("x-ratelimit-reset")
            or headers_lower.get("ratelimit-reset")
        )

        return cls(
            id_requisicao=id_req,
            data_hora=datetime.now(),
            codigo_status=status_code,
            latencia_ms=round(latencia_ms, 2),
            foi_rate_limit=eh_429,
            tempo_espera_retry_after=retry_after,
            limite_declarado=limite,
            limite_restante=restante,
            limite_reset=reset,
            cabecalhos_resposta=headers,
            mensagem_status=motivo_status or f"HTTP {status_code}"
        )

    @classmethod
    def criar_com_falha(
        cls,
        id_req: int,
        latencia_ms: float,
        erro: str
    ) -> "ResultadoRequisicao":
        """Fabrica um resultado para erros de rede, timeout, DNS, SSL, etc."""
        return cls(
            id_requisicao=id_req,
            data_hora=datetime.now(),
            codigo_status=0,
            latencia_ms=round(latencia_ms, 2),
            foi_rate_limit=False,
            mensagem_status="Falha de Conexão",
            mensagem_erro=erro
        )
