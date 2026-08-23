from dataclasses import dataclass
from .configuracao_requisicao import ConfiguracaoRequisicao

@dataclass(frozen=True)
class PlanoTeste:
    """Define o plano de execução da bateria de testes de rate-limit."""
    configuracao: ConfiguracaoRequisicao
    total_requisicoes: int = 50
    concorrencia: int = 5
    intervalo_milissegundos: int = 0

    def __post_init__(self):
        if self.total_requisicoes <= 0:
            raise ValueError("O total de requisições deve ser maior que zero.")
        if self.concorrencia <= 0:
            raise ValueError("A concorrência (threads) deve ser maior que zero.")
        if self.intervalo_milissegundos < 0:
            raise ValueError("O intervalo entre requisições não pode ser negativo.")
        if self.concorrencia > self.total_requisicoes:
            # Ajusta automaticamente para não abrir mais threads que requisições
            object.__setattr__(self, "concorrencia", self.total_requisicoes)
