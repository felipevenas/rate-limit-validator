import unittest
import tkinter as tk
from src.presentation.views.componentes.ajuda_tooltip import Tooltip, BotaoAjuda, criar_rotulo_com_ajuda

class TestAjudaTooltip(unittest.TestCase):
    """Testes unitários para o sistema de balões de ajuda e tooltips."""

    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.root.destroy()
        except Exception:
            pass

    def test_instanciacao_botao_ajuda(self):
        btn = BotaoAjuda(self.root, titulo="Teste Titulo", explicacao="Explicacao de teste")
        self.assertEqual(btn.cget("text"), "(?)")
        self.assertEqual(btn.titulo, "Teste Titulo")
        self.assertEqual(btn.explicacao, "Explicacao de teste")

    def test_criar_rotulo_com_ajuda(self):
        frame, lbl, btn = criar_rotulo_com_ajuda(
            self.root,
            texto_rotulo="Concorrência (Threads):",
            titulo_ajuda="Concorrência",
            texto_ajuda="Número de threads simultâneas."
        )
        self.assertIsInstance(frame, tk.Widget)
        self.assertEqual(lbl.cget("text"), "Concorrência (Threads):")
        self.assertEqual(btn.titulo, "Concorrência")
        self.assertIn("threads", btn.explicacao)

    def test_tooltip_ciclo_vida(self):
        lbl = tk.Label(self.root, text="Alvo")
        tip = Tooltip(lbl, texto="Texto descritivo", titulo="Titulo")
        self.assertIsNone(tip._janela_tooltip)
        
        # Testar exibição e ocultação
        tip.mostrar()
        self.assertIsNotNone(tip._janela_tooltip)
        tip.ocultar()
        self.assertIsNone(tip._janela_tooltip)

if __name__ == "__main__":
    unittest.main()
