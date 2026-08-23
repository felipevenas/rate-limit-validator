import sys
import os

# Garante identificação do processo nativo no Windows para exibir o ícone na barra de tarefas e bandeja
if sys.platform.startswith("win"):
    import ctypes
    try:
        myappid = "apitools.ratelimit.validator.v2"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

# Garante que o diretório raiz do projeto esteja no sys.path
diretorio_raiz = os.path.dirname(os.path.abspath(__file__))
if diretorio_raiz not in sys.path:
    sys.path.insert(0, diretorio_raiz)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from src.infrastructure.http.cliente_http_urllib import ClienteHttpUrllib
from src.infrastructure.exporters.exportador_csv import ExportadorCsv
from src.application.use_cases.executar_teste_rate_limit import ExecutarTesteRateLimitUseCase
from src.presentation.controllers.controlador_qt import ControladorPrincipalQt
from src.presentation.views.janela_principal_qt import JanelaPrincipalQt, criar_icone_aplicacao

def main():
    """
    Ponto de entrada (Composition Root) do Validador de Rate Limit em PySide6.
    Monta a árvore de injeção de dependências seguindo os princípios da Clean Architecture.
    """
    # 1. Configuração da Aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Validador de Rate Limit")
    app.setOrganizationName("API Tools BR")

    icone_app = criar_icone_aplicacao()
    if not icone_app.isNull():
        app.setWindowIcon(icone_app)

    # 2. Camada de Infraestrutura
    cliente_http = ClienteHttpUrllib(ignorar_verificacao_ssl=False)
    exportador_csv = ExportadorCsv()

    # 3. Camada de Aplicação (Casos de Uso)
    caso_de_uso_executar = ExecutarTesteRateLimitUseCase(cliente_http=cliente_http)

    # 4. Camada de Apresentação (Controlador e Janela Mestre Qt)
    controlador = ControladorPrincipalQt(
        caso_de_uso_executar=caso_de_uso_executar,
        exportador_csv=exportador_csv
    )
    janela = JanelaPrincipalQt(controlador=controlador)
    janela.show()

    # 5. Execução do loop de eventos principal
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
