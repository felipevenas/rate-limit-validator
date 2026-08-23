# Changelog 📋

Todas as alterações notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.0.0] - 2026-08-23

### 🚀 Adicionado
- **Migração Completa para PySide6 (Qt for Python)** com arquitetura limpa desacoplada.
- **Design System Premium**: Suporte nativo e instantâneo a **Dark Mode (Minimalist Slate & Indigo)** e **Light Mode (Clean Light)**.
- **Barra de Marca Executiva**: Logotipo minimalista vetorial SVG de alta definição (`app_icon.svg`) e indicador de status reativo no topo.
- **Botões de Ajuda Interativos (?)**: Tooltips HTML ricas e caixas de diálogo explicativas para todos os parâmetros (Threads, Rate Limit 429, Timeout, Latência, RPS, etc.).
- **Tabela em Tempo Real**:
  - Inserção dinâmica a cada resposta recebida.
  - Filtros rápidos por tipo (Todos, 2xx, 429, Erros).
  - Busca textual em tempo real por ID, status HTTP e mensagens de erro.
  - Ordenação dinâmica por clique no cabeçalho das colunas.
- **Painel de Métricas Avançado**: Indicadores de progresso, sucessos 2xx, bloqueios 429, falhas, latência média e vazão RPS.
- **Integração com a Bandeja do Sistema (System Tray)**:
  - Ícone nativo na bandeja do Windows (`QSystemTrayIcon`).
  - Menu de contexto (Restaurar, Alternar Tema, Sair).
  - Notificações balão automáticas ao concluir baterias de testes.
  - Registro de `SetCurrentProcessExplicitAppUserModelID` no Windows para exibição de ícone oficial na Barra de Tarefas e Alt+Tab.
- **Exportação de Relatórios CSV**: Exportação estruturada com resumo estatístico e registros linha a linha.
- **Esteira de CI/CD**: Workflow no GitHub Actions para execução de testes em matriz multiplataforma e compilação/publicação automática de executáveis Windows (`.exe`).
- **Governança Multi-Agente**: Adicionado ecossistema completo em `.agents/` com 7 agentes especializados (`tech-lead`, `software-architect`, `backend-dev`, `frontend-dev`, `ux-ui-designer`, `qa-engineer`, `security-engineer`).

---

## [1.0.0] - 2026-08-22

### 🚀 Versão Inicial
- Versão inicial com core de testes de concorrência e detecção de políticas de Rate Limit.
