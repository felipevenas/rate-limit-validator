from dataclasses import dataclass, field
from typing import Dict, Optional
import json

@dataclass(frozen=True)
class ConfiguracaoRequisicao:
    """Representa os dados de configuração de uma requisição HTTP a ser disparada."""
    url: str
    metodo: str = "GET"
    cabecalhos: Dict[str, str] = field(default_factory=dict)
    corpo: Optional[str] = None
    tempo_limite_segundos: float = 10.0

    def __post_init__(self):
        url_limpa = self.url.strip()
        if not url_limpa:
            raise ValueError("A URL do endpoint não pode ser vazia.")
        if not (url_limpa.startswith("http://") or url_limpa.startswith("https://")):
            raise ValueError("A URL deve iniciar com 'http://' ou 'https://'.")

        metodo_upper = self.metodo.upper().strip()
        metodos_permitidos = {"GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"}
        if metodo_upper not in metodos_permitidos:
            raise ValueError(f"Método HTTP inválido: {self.metodo}. Permitidos: {', '.join(sorted(metodos_permitidos))}")

        object.__setattr__(self, "url", url_limpa)
        object.__setattr__(self, "metodo", metodo_upper)

        if self.corpo and self.corpo.strip():
            # Validação amigável se for um JSON declarado
            content_type = self.cabecalhos.get("Content-Type", "") or self.cabecalhos.get("content-type", "")
            if "application/json" in content_type.lower():
                try:
                    json.loads(self.corpo)
                except Exception as e:
                    raise ValueError(f"Corpo da requisição não é um JSON válido: {e}")
