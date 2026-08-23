from dataclasses import dataclass, field
from typing import List
from .resultado_requisicao import ResultadoRequisicao

@dataclass
class ResumoMetricas:
    """Agrega e calcula estatísticas sobre os resultados dos testes."""
    total_enviadas: int = 0
    total_esperado: int = 0
    sucessos_2xx: int = 0
    bloqueios_429: int = 0
    outros_erros: int = 0
    latencias: List[float] = field(default_factory=list)
    tempo_total_segundos: float = 0.0

    def adicionar_resultado(self, resultado: ResultadoRequisicao) -> None:
        """Processa um novo resultado de requisição recebido."""
        self.total_enviadas += 1
        self.latencias.append(resultado.latencia_ms)

        if 200 <= resultado.codigo_status <= 299:
            self.sucessos_2xx += 1
        elif resultado.foi_rate_limit:
            self.bloqueios_429 += 1
        else:
            self.outros_erros += 1

    @property
    def percentual_concluido(self) -> float:
        if self.total_esperado <= 0:
            return 0.0
        return min(100.0, (self.total_enviadas / self.total_esperado) * 100.0)

    @property
    def latencia_media_ms(self) -> float:
        if not self.latencias:
            return 0.0
        return round(sum(self.latencias) / len(self.latencias), 2)

    @property
    def latencia_minima_ms(self) -> float:
        if not self.latencias:
            return 0.0
        return round(min(self.latencias), 2)

    @property
    def latencia_maxima_ms(self) -> float:
        if not self.latencias:
            return 0.0
        return round(max(self.latencias), 2)

    @property
    def requisicoes_por_segundo(self) -> float:
        if self.tempo_total_segundos <= 0:
            return 0.0
        return round(self.total_enviadas / self.tempo_total_segundos, 2)
