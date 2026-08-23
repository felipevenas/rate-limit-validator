from abc import ABC, abstractmethod
from ..entities.resultado_requisicao import ResultadoRequisicao
from ..entities.resumo_metricas import ResumoMetricas

class INotificadorProgresso(ABC):
    """Contrato abstrato para notificação de progresso e métricas em tempo de execução."""

    @abstractmethod
    def notificar_item_processado(self, resultado: ResultadoRequisicao, metricas: ResumoMetricas) -> None:
        """Chamado a cada requisição individual concluída."""
        pass

    @abstractmethod
    def notificar_teste_concluido(self, metricas: ResumoMetricas, cancelado: bool = False) -> None:
        """Chamado quando toda a bateria de testes finaliza ou é cancelada."""
        pass
