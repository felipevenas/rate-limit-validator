import unittest
import os
import tempfile
from src.domain.entities.resultado_requisicao import ResultadoRequisicao
from src.domain.entities.resumo_metricas import ResumoMetricas
from src.infrastructure.exporters.exportador_csv import ExportadorCsv

class TestExportadorCsv(unittest.TestCase):

    def test_exportacao_csv(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_path = temp_file.name

        try:
            metricas = ResumoMetricas(total_enviadas=2, total_esperado=2, sucessos_2xx=1, bloqueios_429=1)
            r1 = ResultadoRequisicao.criar_com_sucesso(1, 200, 45.0, {})
            r2 = ResultadoRequisicao.criar_com_sucesso(2, 429, 30.0, {"Retry-After": "10"})
            resultados = [r1, r2]

            ExportadorCsv.exportar(temp_path, resultados, metricas)

            self.assertTrue(os.path.exists(temp_path))
            with open(temp_path, "r", encoding="utf-8-sig") as f:
                conteudo = f.read()

            self.assertIn("RELATÓRIO DE VALIDAÇÃO DE RATE LIMIT", conteudo)
            self.assertIn("Bloqueios por Rate Limit (429)", conteudo)
            self.assertIn("Retry-After", conteudo)
            self.assertIn("10", conteudo)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    unittest.main()
