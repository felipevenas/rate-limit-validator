import os
import sys

def obter_caminho_recurso(caminho_relativo: str) -> str:
    """Retorna o caminho absoluto do recurso, compatível com desenvolvimento e empacotamento PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        caminho_base = sys._MEIPASS
    else:
        caminho_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    return os.path.abspath(os.path.join(caminho_base, caminho_relativo)).replace("\\", "/")

DIRETORIO_ICONES = obter_caminho_recurso("src/presentation/assets/icons")

def gerar_tema_dark() -> str:
    return f"""
/* ==========================================================================
   TEMA PREMIUM DARK (Minimalist Slate & Indigo)
   ========================================================================== */

/* Regra Geral: Fundo transparente por padrão para evitar retângulos recortados */
QWidget {{
    background: transparent;
    color: #f1f5f9;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    font-size: 13px;
    outline: none;
}}

/* Janela Principal e Canvas de Scroll */
QMainWindow, QScrollArea, QWidget#conteudo_scroll {{
    background-color: #0a0b0e;
}}

/* === CABEÇALHO / HEADER BRAND === */
QWidget#container_header_brand {{
    background-color: #13151c;
    border: 1px solid #202432;
    border-radius: 10px;
    padding: 6px 14px;
}}

QLabel#lbl_titulo_brand {{
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: 0.3px;
}}

QLabel#lbl_subtitulo_brand {{
    font-size: 11px;
    color: #94a3b8;
}}

QLabel#lbl_badge_status_header {{
    background-color: #0c0d12;
    border: 1px solid #202432;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    color: #10b981;
}}

/* === GROUPBOX (CARDS DE SEÇÃO ELEVADOS) === */
QGroupBox {{
    background-color: #13151c;
    border: 1px solid #202432;
    border-radius: 10px;
    margin-top: 16px;
    padding-top: 18px;
    padding-left: 14px;
    padding-right: 14px;
    padding-bottom: 14px;
    font-weight: 600;
    font-size: 12px;
    color: #e2e8f0;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 3px 10px;
    background-color: #1c1f2b;
    border: 1px solid #2a3042;
    border-radius: 5px;
    color: #cbd5e1;
    font-size: 12px;
}}

/* === ROTULOS E LABELS === */
QLabel {{
    background: transparent;
}}

QLabel#lbl_destaque {{
    color: #f1f5f9;
    font-weight: 600;
    font-size: 12px;
}}

QLabel#lbl_parametro {{
    color: #94a3b8;
    font-size: 12px;
    font-weight: 500;
}}

/* === BOTÃO DE AJUDA (?) === */
QPushButton#btn_ajuda {{
    background-color: #1a1d28;
    color: #94a3b8;
    border: 1px solid #2a3042;
    border-radius: 9px;
    font-weight: bold;
    font-size: 10px;
    padding: 0;
    margin: 0;
}}

QPushButton#btn_ajuda:hover {{
    background-color: #4f46e5;
    color: #ffffff;
    border-color: #6366f1;
}}

QPushButton#btn_ajuda:pressed {{
    background-color: #3730a3;
}}

/* === CARDS DE MÉTRICAS === */
QFrame#card_metrica {{
    background-color: #0c0d12;
    border: 1px solid #1e2230;
    border-radius: 8px;
    padding: 6px 8px;
}}

QFrame#card_metrica:hover {{
    border-color: #31384d;
}}

QLabel#lbl_card_titulo {{
    color: #94a3b8;
    font-size: 11px;
    font-weight: 600;
}}

QLabel#lbl_card_ponto {{
    font-size: 10px;
    padding: 0;
}}

QLabel#lbl_card_valor {{
    font-size: 19px;
    font-weight: 700;
    padding: 2px 0;
}}

/* Cores Semânticas das Métricas */
QLabel#lbl_card_ponto[metrica_tipo="sucesso"], QLabel#lbl_card_valor[metrica_tipo="sucesso"] {{
    color: #10b981;
}}

QLabel#lbl_card_ponto[metrica_tipo="rate_limit"], QLabel#lbl_card_valor[metrica_tipo="rate_limit"] {{
    color: #f43f5e;
}}

QLabel#lbl_card_ponto[metrica_tipo="erro"], QLabel#lbl_card_valor[metrica_tipo="erro"] {{
    color: #fb923c;
}}

QLabel#lbl_card_ponto[metrica_tipo="latencia"], QLabel#lbl_card_valor[metrica_tipo="latencia"] {{
    color: #38bdf8;
}}

QLabel#lbl_card_ponto[metrica_tipo="rps"], QLabel#lbl_card_valor[metrica_tipo="rps"] {{
    color: #a78bfa;
}}

/* === CAMPOS DE ENTRADA (QLineEdit) === */
QLineEdit {{
    background-color: #0c0d12;
    color: #f8fafc;
    border: 1px solid #242938;
    border-radius: 6px;
    padding: 5px 10px;
    min-height: 28px;
    max-height: 28px;
    font-size: 13px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}}

QLineEdit:hover {{
    border-color: #384056;
}}

QLineEdit:focus {{
    border: 1px solid #6366f1;
    background-color: #10121a;
}}

QLineEdit:disabled {{
    background-color: #14161e;
    color: #4b5563;
    border-color: #1e2230;
}}

/* === SELETOR (QComboBox) === */
QComboBox {{
    background-color: #0c0d12;
    color: #f8fafc;
    border: 1px solid #242938;
    border-radius: 6px;
    padding: 5px 28px 5px 10px;
    min-height: 28px;
    max-height: 28px;
    font-size: 13px;
}}

QComboBox:hover {{
    border-color: #384056;
}}

QComboBox:focus {{
    border: 1px solid #6366f1;
    background-color: #10121a;
}}

QComboBox:disabled {{
    background-color: #14161e;
    color: #4b5563;
    border-color: #1e2230;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 1px solid #1e2230;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    background-color: #13151c;
}}

QComboBox::drop-down:hover {{
    background-color: #1c1f2b;
}}

QComboBox::down-arrow {{
    image: url("{DIRETORIO_ICONES}/chevron-down.svg");
    width: 12px;
    height: 12px;
}}

QComboBox QAbstractItemView {{
    background-color: #13151c;
    color: #f8fafc;
    border: 1px solid #2a3042;
    border-radius: 6px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
    padding: 4px;
}}

/* === CONTROLE NUMÉRICO (QSpinBox) === */
QSpinBox {{
    background-color: #0c0d12;
    color: #f8fafc;
    border: 1px solid #242938;
    border-radius: 6px;
    padding: 5px 24px 5px 10px;
    min-height: 28px;
    max-height: 28px;
    font-size: 13px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}}

QSpinBox:hover {{
    border-color: #384056;
}}

QSpinBox:focus {{
    border: 1px solid #6366f1;
    background-color: #10121a;
}}

QSpinBox:disabled {{
    background-color: #14161e;
    color: #4b5563;
    border-color: #1e2230;
}}

QSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid #1e2230;
    border-bottom: 1px solid #1e2230;
    border-top-right-radius: 5px;
    background-color: #13151c;
}}

QSpinBox::up-button:hover {{
    background-color: #1c1f2b;
}}

QSpinBox::up-arrow {{
    image: url("{DIRETORIO_ICONES}/chevron-up.svg");
    width: 10px;
    height: 10px;
}}

QSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 22px;
    border-left: 1px solid #1e2230;
    border-bottom-right-radius: 5px;
    background-color: #13151c;
}}

QSpinBox::down-button:hover {{
    background-color: #1c1f2b;
}}

QSpinBox::down-arrow {{
    image: url("{DIRETORIO_ICONES}/chevron-down.svg");
    width: 10px;
    height: 10px;
}}

/* === ÁREAS DE TEXTO (QTextEdit) === */
QTextEdit {{
    background-color: #0c0d12;
    color: #f8fafc;
    border: 1px solid #242938;
    border-radius: 6px;
    padding: 8px;
    font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}}

QTextEdit:focus {{
    border: 1px solid #6366f1;
    background-color: #10121a;
}}

/* === ABAS SEGMENTADAS (QTabWidget) === */
QTabWidget::pane {{
    border: 1px solid #202432;
    border-radius: 6px;
    background-color: #13151c;
    top: -1px;
}}

QTabBar::tab {{
    background-color: #0c0d12;
    color: #94a3b8;
    border: 1px solid #202432;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 6px 14px;
    margin-right: 3px;
    font-weight: 600;
    font-size: 12px;
}}

QTabBar::tab:selected {{
    background-color: #13151c;
    color: #f1f5f9;
    border-color: #31384d;
    border-top: 2px solid #6366f1;
}}

QTabBar::tab:hover:!selected {{
    background-color: #171922;
    color: #cbd5e1;
}}

/* === BOTÕES (QPushButton) === */
QPushButton {{
    background-color: #191c26;
    color: #e2e8f0;
    border: 1px solid #2a3042;
    border-radius: 6px;
    padding: 6px 16px;
    min-height: 26px;
    font-weight: 600;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: #242838;
    border-color: #384056;
    color: #ffffff;
}}

QPushButton:pressed {{
    background-color: #13151c;
}}

QPushButton:disabled {{
    background-color: #13151c;
    color: #4b5563;
    border-color: #1e2230;
}}

/* Botão Primário (Iniciar) */
QPushButton#btn_iniciar {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #4338ca);
    border: 1px solid #6366f1;
    color: #ffffff;
    font-size: 12px;
    font-weight: bold;
    padding: 6px 20px;
}}

QPushButton#btn_iniciar:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #4f46e5);
    border-color: #818cf8;
}}

/* Botão Perigo (Interromper) */
QPushButton#btn_cancelar {{
    background-color: #1b1215;
    border: 1px solid #7f1d1d;
    color: #f87171;
    padding: 6px 18px;
}}

QPushButton#btn_cancelar:hover {{
    background-color: #991b1b;
    border-color: #ef4444;
    color: #ffffff;
}}

/* === BARRA DE PROGRESSO === */
QProgressBar {{
    background-color: #0c0d12;
    border: 1px solid #202432;
    border-radius: 4px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    min-height: 10px;
    max-height: 10px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #6366f1);
    border-radius: 3px;
}}

/* === TABELA DE REGISTROS (QTableWidget) === */
QTableWidget {{
    background-color: #0c0d12;
    alternate-background-color: #10121a;
    border: 1px solid #202432;
    border-radius: 7px;
    gridline-color: #171a24;
    color: #e2e8f0;
    selection-background-color: #1b2030;
    selection-color: #ffffff;
}}

QHeaderView::section {{
    background-color: #13151c;
    color: #94a3b8;
    font-weight: 600;
    font-size: 11px;
    border: none;
    border-right: 1px solid #202432;
    border-bottom: 1px solid #202432;
    padding: 6px 8px;
}}

QHeaderView::section:hover {{
    background-color: #1a1d28;
    color: #f1f5f9;
}}

/* === CHECKBOX === */
QCheckBox {{
    color: #cbd5e1;
    spacing: 6px;
    font-size: 12px;
}}

QCheckBox::indicator {{
    width: 15px;
    height: 15px;
    border: 1px solid #384056;
    border-radius: 4px;
    background-color: #0c0d12;
}}

QCheckBox::indicator:checked {{
    image: url("{DIRETORIO_ICONES}/check.svg");
    background-color: #4f46e5;
    border-color: #6366f1;
}}

/* === STATUS BAR E LABELS DE CONTROLE === */
QStatusBar {{
    background-color: #0a0b0e;
    border-top: 1px solid #1a1d28;
    color: #64748b;
    font-size: 11px;
}}

QLabel#lbl_status {{
    color: #38bdf8;
    font-weight: 500;
    font-size: 12px;
}}

QLabel#lbl_status[status_tipo="executando"] {{
    color: #facc15;
    font-weight: bold;
}}

QLabel#lbl_status[status_tipo="sucesso"] {{
    color: #4ade80;
    font-weight: bold;
}}

QLabel#lbl_status[status_tipo="erro"], QLabel#lbl_status[status_tipo="cancelado"] {{
    color: #f87171;
    font-weight: bold;
}}

QPushButton#btn_tema {{
    background-color: #13151c;
    color: #cbd5e1;
    border: 1px solid #242938;
    border-radius: 4px;
    font-size: 11px;
    padding: 3px 10px;
}}

QPushButton#btn_tema:hover {{
    background-color: #1e2230;
    color: #ffffff;
}}

QLabel#lbl_icone_busca, QLabel#lbl_filtro_titulo, QLabel#lbl_contagem_tabela {{
    color: #94a3b8;
}}
"""

def gerar_tema_light() -> str:
    return f"""
/* ==========================================================================
   TEMA PREMIUM LIGHT (Clean Apple & Stripe Style)
   ========================================================================== */

QWidget {{
    background: transparent;
    color: #0f172a;
    font-family: 'Segoe UI Variable Text', 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    font-size: 13px;
    outline: none;
}}

QMainWindow, QScrollArea, QWidget#conteudo_scroll {{
    background-color: #f1f5f9;
}}

/* === CABEÇALHO / HEADER BRAND === */
QWidget#container_header_brand {{
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 6px 14px;
}}

QLabel#lbl_titulo_brand {{
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: 0.3px;
}}

QLabel#lbl_subtitulo_brand {{
    font-size: 11px;
    color: #64748b;
}}

QLabel#lbl_badge_status_header {{
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
    color: #15803d;
}}

/* === GROUPBOX === */
QGroupBox {{
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    margin-top: 16px;
    padding-top: 18px;
    padding-left: 14px;
    padding-right: 14px;
    padding-bottom: 14px;
    font-weight: 600;
    font-size: 12px;
    color: #1e293b;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 3px 10px;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    color: #334155;
    font-size: 12px;
}}

/* === ROTULOS E LABELS === */
QLabel {{
    background: transparent;
}}

QLabel#lbl_destaque {{
    color: #0f172a;
    font-weight: 600;
    font-size: 12px;
}}

QLabel#lbl_parametro {{
    color: #64748b;
    font-size: 12px;
    font-weight: 500;
}}

/* === BOTÃO DE AJUDA (?) === */
QPushButton#btn_ajuda {{
    background-color: #e2e8f0;
    color: #475569;
    border: 1px solid #cbd5e1;
    border-radius: 9px;
    font-weight: bold;
    font-size: 10px;
    padding: 0;
    margin: 0;
}}

QPushButton#btn_ajuda:hover {{
    background-color: #4f46e5;
    color: #ffffff;
    border-color: #4338ca;
}}

QPushButton#btn_ajuda:pressed {{
    background-color: #3730a3;
}}

/* === CARDS DE MÉTRICAS === */
QFrame#card_metrica {{
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 6px 8px;
}}

QFrame#card_metrica:hover {{
    border-color: #cbd5e1;
}}

QLabel#lbl_card_titulo {{
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
}}

QLabel#lbl_card_ponto {{
    font-size: 10px;
    padding: 0;
}}

QLabel#lbl_card_valor {{
    font-size: 19px;
    font-weight: 700;
    padding: 2px 0;
}}

/* Cores Semânticas das Métricas */
QLabel#lbl_card_ponto[metrica_tipo="sucesso"], QLabel#lbl_card_valor[metrica_tipo="sucesso"] {{
    color: #16a34a;
}}

QLabel#lbl_card_ponto[metrica_tipo="rate_limit"], QLabel#lbl_card_valor[metrica_tipo="rate_limit"] {{
    color: #e11d48;
}}

QLabel#lbl_card_ponto[metrica_tipo="erro"], QLabel#lbl_card_valor[metrica_tipo="erro"] {{
    color: #ea580c;
}}

QLabel#lbl_card_ponto[metrica_tipo="latencia"], QLabel#lbl_card_valor[metrica_tipo="latencia"] {{
    color: #0284c7;
}}

QLabel#lbl_card_ponto[metrica_tipo="rps"], QLabel#lbl_card_valor[metrica_tipo="rps"] {{
    color: #7c3aed;
}}

/* === CAMPOS DE ENTRADA === */
QLineEdit {{
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 10px;
    min-height: 28px;
    max-height: 28px;
    font-size: 13px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}}

QLineEdit:hover {{
    border-color: #94a3b8;
}}

QLineEdit:focus {{
    border: 1px solid #4f46e5;
    background-color: #ffffff;
}}

QComboBox {{
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 28px 5px 10px;
    min-height: 28px;
    max-height: 28px;
    font-size: 13px;
}}

QComboBox:focus {{
    border: 1px solid #4f46e5;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border-left: 1px solid #e2e8f0;
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
    background-color: #f8fafc;
}}

QComboBox::down-arrow {{
    image: url("{DIRETORIO_ICONES}/chevron-down.svg");
    width: 12px;
    height: 12px;
}}

QSpinBox {{
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 5px 24px 5px 10px;
    min-height: 28px;
    max-height: 28px;
    font-size: 13px;
}}

QSpinBox:focus {{
    border: 1px solid #4f46e5;
}}

QSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 22px;
    border-left: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    border-top-right-radius: 5px;
    background-color: #f8fafc;
}}

QSpinBox::up-arrow {{
    image: url("{DIRETORIO_ICONES}/chevron-up.svg");
    width: 10px;
    height: 10px;
}}

QSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 22px;
    border-left: 1px solid #e2e8f0;
    border-bottom-right-radius: 5px;
    background-color: #f8fafc;
}}

QSpinBox::down-arrow {{
    image: url("{DIRETORIO_ICONES}/chevron-down.svg");
    width: 10px;
    height: 10px;
}}

QTextEdit {{
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 8px;
    font-family: 'Cascadia Code', 'Consolas', 'Courier New', monospace;
    font-size: 12px;
}}

QTextEdit:focus {{
    border: 1px solid #4f46e5;
}}

QPushButton {{
    background-color: #f1f5f9;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 16px;
    min-height: 26px;
    font-weight: 600;
    font-size: 12px;
}}

QPushButton:hover {{
    background-color: #e2e8f0;
    color: #0f172a;
}}

QPushButton#btn_iniciar {{
    background-color: #4f46e5;
    border: 1px solid #4338ca;
    color: #ffffff;
    font-weight: bold;
    padding: 6px 20px;
}}

QPushButton#btn_iniciar:hover {{
    background-color: #4338ca;
}}

QPushButton#btn_cancelar {{
    background-color: #fef2f2;
    border: 1px solid #fca5a5;
    color: #dc2626;
    padding: 6px 18px;
}}

QPushButton#btn_cancelar:hover {{
    background-color: #ef4444;
    color: #ffffff;
}}

QProgressBar {{
    background-color: #e2e8f0;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    text-align: center;
    color: #0f172a;
    font-weight: bold;
    min-height: 10px;
    max-height: 10px;
}}

QProgressBar::chunk {{
    background-color: #4f46e5;
    border-radius: 3px;
}}

QTableWidget {{
    background-color: #ffffff;
    alternate-background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 7px;
    gridline-color: #f1f5f9;
    color: #1e293b;
    selection-background-color: #eef2ff;
    selection-color: #4338ca;
}}

QHeaderView::section {{
    background-color: #f8fafc;
    color: #64748b;
    font-weight: 600;
    font-size: 11px;
    border: none;
    border-right: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    padding: 6px 8px;
}}

QCheckBox::indicator:checked {{
    image: url("{DIRETORIO_ICONES}/check.svg");
    background-color: #4f46e5;
    border-color: #4338ca;
}}

QStatusBar {{
    background-color: #f1f5f9;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
}}

QLabel#lbl_status {{
    color: #0284c7;
    font-weight: 500;
    font-size: 12px;
}}

QLabel#lbl_status[status_tipo="executando"] {{
    color: #ca8a04;
    font-weight: bold;
}}

QLabel#lbl_status[status_tipo="sucesso"] {{
    color: #15803d;
    font-weight: bold;
}}

QLabel#lbl_status[status_tipo="erro"], QLabel#lbl_status[status_tipo="cancelado"] {{
    color: #dc2626;
    font-weight: bold;
}}

QPushButton#btn_tema {{
    background-color: #ffffff;
    color: #334155;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    font-size: 11px;
    padding: 3px 10px;
}}

QPushButton#btn_tema:hover {{
    background-color: #e2e8f0;
}}

QLabel#lbl_icone_busca, QLabel#lbl_filtro_titulo, QLabel#lbl_contagem_tabela {{
    color: #64748b;
}}
"""

TEMA_DARK = gerar_tema_dark()
TEMA_LIGHT = gerar_tema_light()
