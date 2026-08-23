from abc import ABC, abstractmethod
from ..entities.configuracao_requisicao import ConfiguracaoRequisicao
from ..entities.resultado_requisicao import ResultadoRequisicao

class IClienteHttp(ABC):
    """Contrato abstrato para clientes HTTP responsáveis pelo envio físico de requisições."""

    @abstractmethod
    def enviar(self, config: ConfiguracaoRequisicao, id_requisicao: int) -> ResultadoRequisicao:
        """Executa o envio de uma requisição HTTP e retorna o resultado padronizado."""
        pass
