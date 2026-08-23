import os
import sys
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize

def gerar_ico():
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    caminho_svg = os.path.join(raiz, "src", "presentation", "assets", "icons", "app_icon.svg")
    caminho_ico = os.path.join(raiz, "src", "presentation", "assets", "icons", "app_icon.ico")
    caminho_png = os.path.join(raiz, "src", "presentation", "assets", "icons", "app_icon.png")

    if not os.path.exists(caminho_svg):
        print(f"Erro: SVG não encontrado em {caminho_svg}")
        return False

    renderer = QSvgRenderer(caminho_svg)
    if not renderer.isValid():
        print("Erro: SVG inválido!")
        return False

    # Renderiza PNG de alta resolução (256x256)
    img_256 = QImage(256, 256, QImage.Format_ARGB32)
    img_256.fill(0)
    painter = QPainter(img_256)
    renderer.render(painter)
    painter.end()

    img_256.save(caminho_png, "PNG")
    print(f"[OK] PNG gerado em: {caminho_png}")

    # Salva também como ICO
    img_256.save(caminho_ico, "ICO")
    print(f"[OK] ICO gerado em: {caminho_ico}")
    return True

if __name__ == "__main__":
    gerar_ico()
