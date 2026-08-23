import csv
from typing import List
from ...domain.entities.resultado_requisicao import ResultadoRequisicao
from ...domain.entities.resumo_metricas import ResumoMetricas

class ExportadorCsv:
    """Exportador para gravação de relatórios de teste em formato CSV."""

    @staticmethod
    def exportar(caminho_arquivo: str, resultados: List[ResultadoRequisicao], metricas: ResumoMetricas) -> None:
        """Gera o arquivo CSV com resumo estatístico e tabela detalhada de requisições."""
        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
            escritor = csv.writer(f, delimiter=";")

            # Cabeçalho de Metadados / Resumo
            escritor.writerow(["=== RELATÓRIO DE VALIDAÇÃO DE RATE LIMIT ==="])
            escritor.writerow(["Total de Requisições Enviadas", metricas.total_enviadas])
            escritor.writerow(["Sucessos (2xx)", metricas.sucessos_2xx])
            escritor.writerow(["Bloqueios por Rate Limit (429)", metricas.bloqueios_429])
            escritor.writerow(["Erros / Falhas de Conexão", metricas.outros_erros])
            escritor.writerow(["Tempo Total de Execução (s)", f"{metricas.tempo_total_segundos:.2f}"])
            escritor.writerow(["Requisições por Segundo (RPS)", f"{metricas.requisicoes_por_segundo:.2f}"])
            escritor.writerow(["Latência Média (ms)", f"{metricas.latencia_media_ms:.2f}"])
            escritor.writerow(["Latência Mínima (ms)", f"{metricas.latencia_minima_ms:.2f}"])
            escritor.writerow(["Latência Máxima (ms)", f"{metricas.latencia_maxima_ms:.2f}"])
            escritor.writerow([])

            # Cabeçalho da Tabela de Detalhes
            escritor.writerow([
                "ID",
                "Data e Hora",
                "Código de Status",
                "Situação",
                "Latência (ms)",
                "Rate Limit?",
                "Retry-After",
                "Limite Declarado",
                "Limite Restante",
                "Limite Reset",
                "Detalhe / Mensagem de Erro"
            ])

            # Linhas de Dados
            for res in resultados:
                situacao = "Rate Limit (429)" if res.foi_rate_limit else (
                    "Sucesso (2xx)" if 200 <= res.codigo_status <= 299 else "Erro/Falha"
                )
                escritor.writerow([
                    res.id_requisicao,
                    res.data_hora.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
                    res.codigo_status if res.codigo_status > 0 else "N/A",
                    situacao,
                    f"{res.latencia_ms:.2f}",
                    "SIM" if res.foi_rate_limit else "NÃO",
                    res.tempo_espera_retry_after or "-",
                    res.limite_declarado or "-",
                    res.limite_restante or "-",
                    res.limite_reset or "-",
                    res.mensagem_erro or res.mensagem_status
                ])
