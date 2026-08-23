<div align="center">

# Rate Limit Validator & Stress Tester ⚡🛡️

**Software Desktop de Alta Performance para Teste de Concorrência, Validação de Políticas de Rate Limit e Resiliência de APIs REST**

[![CI Status](https://img.shields.io/badge/CI-Passing-brightgreen?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/felipevenas/rate-limit-validator/actions)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/Framework-PySide6%20%2F%20Qt-41cd52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v2.0.0-orange?style=for-the-badge&logo=github&logoColor=white)](https://github.com/felipevenas/rate-limit-validator/releases)

<br />

<p align="center">
  <a href="#-download-do-executável-windows-exe"><b>Download (.exe)</b></a> •
  <a href="#-principais-funcionalidades"><b>Funcionalidades</b></a> •
  <a href="#️-arquitetura-do-projeto"><b>Arquitetura</b></a> •
  <a href="#-como-executar-localmente"><b>Executar Local</b></a> •
  <a href="#-governança-e-comunidade"><b>Governança</b></a>
</p>

</div>

---

## 💾 Download do Executável Windows (.exe)

Para quem **não possui Python instalado** ou deseja executar o aplicativo de forma portátil no Windows:

1. Acesse a aba de **[Releases Oficiais](https://github.com/felipevenas/rate-limit-validator/releases)**.
2. Baixe o arquivo **`ValidadorRateLimit.exe`**.
3. Dê dois cliques para abrir (arquivo 100% autônomo, sem instaladores ou dependências).

---

## 🌟 Principais Funcionalidades

- **Interface Gráfica Moderna e Responsiva em PySide6**:
  - Logotipo executivo minimalista vetorial SVG.
  - Alternador dinâmico de temas: **Dark Mode (Minimalist Slate & Indigo)** e **Light Mode (Clean Light)**.
  - Integração com a **Bandeja do Sistema (System Tray)** e notificações nativas do Windows.
- **Botões de Ajuda Interativos (?)**:
  - Tooltips HTML ricas e caixas de diálogo explicativas sobre todos os parâmetros técnicos (**Concorrência / Threads**, **Rate Limit 429**, **Timeout**, **Latência**, **RPS**, etc.).
- **Tabela em Tempo Real**:
  - **Inserção instantânea** a cada resposta recebida sem travamentos na UI (60 FPS).
  - **Filtros rápidos por categoria**: Todos, Apenas Sucessos (`2xx`), Apenas Rate Limit (`429`), Apenas Erros/Falhas.
  - **Busca textual em tempo real** por ID, código HTTP ou mensagem.
  - **Ordenação dinâmica** com um clique no cabeçalho das colunas.
- **Métricas em Tempo Real**:
  - Total Enviadas vs Total Esperado e Barra de Progresso animada.
  - Contagem de Sucessos (`2xx`), Bloqueios por Rate Limit (`429`) e Falhas de Rede/Timeouts.
  - Latência Média (ms) e Taxa Efetiva de Vazão (RPS - Requisições por Segundo).
- **Exportação de Relatórios**: Gera relatórios estruturados em formato **CSV** com resumo estatístico e registros linha a linha.

---

## 🏛️ Arquitetura do Projeto

O projeto é estruturado com base nos princípios de **Clean Architecture**, **Domain-Driven Design (DDD)** e **SOLID**:

```text
validador_rate_limit/
├── .agents/                            # Governança Multi-Agente especializada
│   ├── tech-lead/                      # Liderança técnica e decomposição de tarefas
│   ├── software-architect/             # Diretrizes arquiteturais e ADRs
│   ├── backend-dev/                    # Core Python, ThreadPool e protocolos HTTP
│   ├── frontend-dev/                   # Componentização PySide6, Signals & Slots
│   ├── ux-ui-designer/                 # Design System QSS e identidade visual
│   ├── qa-engineer/                    # Baterias de testes e auditoria de qualidade
│   └── security-engineer/              # SSL/TLS, timeouts e integridade de conexões
│
├── .github/                            # Automações e Governança do GitHub
│   ├── workflows/
│   │   ├── ci.yml                      # CI de testes unitários multiplataforma
│   │   ├── build_release.yml           # CI/CD para compilar o .exe nas Releases
│   │   └── labels.yml                  # Sincronizador de labels de issues e PRs
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md               # Template oficial de bugs
│   │   └── feature_request.md          # Template oficial de novas funcionalidades
│   └── PULL_REQUEST_TEMPLATE.md        # Template oficial de Pull Requests
│
├── src/
│   ├── domain/                         # Camada de Domínio (Entidades e Regras Puras)
│   │   ├── entities/
│   │   │   ├── configuracao_requisicao.py  # Value Object de configuração HTTP
│   │   │   ├── plano_teste.py              # Plano de carga (Total, Threads, Delay)
│   │   │   ├── resultado_requisicao.py     # Resultado individual e detecção 429
│   │   │   └── resumo_metricas.py          # Agregador estatístico em tempo real
│   │   └── interfaces/
│   │       ├── cliente_http.py             # Contrato IClienteHttp
│   │       └── notificador_progresso.py    # Contrato INotificadorProgresso
│   │
│   ├── application/                    # Camada de Aplicação (Casos de Uso)
│   │   └── use_cases/
│   │       └── executar_teste_rate_limit.py # Orquestrador com ThreadPoolExecutor
│   │
│   ├── infrastructure/                 # Camada de Infraestrutura (I/O e Rede)
│   │   ├── http/
│   │   │   └── cliente_http_urllib.py      # Cliente HTTP padrão com parsing RFC 6585
│   │   └── exporters/
│   │       └── exportador_csv.py           # Exportador de relatórios CSV
│   │
│   └── presentation/                   # Camada de Apresentação (PySide6 / Qt)
│       ├── assets/icons/               # Ícones vetoriais SVG, PNG e ICO
│       ├── styles/
│       │   └── tema.py                     # Design System QSS (Dark/Light)
│       ├── controllers/
│       │   └── controlador_qt.py           # Controlador reativo via Signals e Slots
│       └── views/
│           ├── componentes/
│           │   ├── botao_ajuda_qt.py           # Botão (?) com tooltips HTML ricas
│           │   ├── formulario_configuracao_qt.py # Formulário de parâmetros
│           │   ├── painel_metricas_qt.py         # Cards de indicadores
│           │   └── tabela_historico_qt.py        # Tabela com busca e filtros
│           └── janela_principal_qt.py            # Janela mestre QMainWindow e Tray
│
├── scripts/
│   ├── gerar_icone_ico.py              # Conversor de SVG para ICO/PNG
│   └── build_executavel.py             # Compilação automatizada do .exe
├── tests/                              # Testes automatizados (Unit & Integration)
├── .env.example                        # Exemplo de variáveis de ambiente
├── .gitignore                          # Arquivos e diretórios ignorados pelo Git
├── CHANGELOG.md                        # Histórico de alterações e releases
├── CODE_OF_CONDUCT.md                  # Código de conduta da comunidade
├── CONTRIBUTING.md                     # Guia de contribuição e desenvolvimento
├── LICENSE                             # Licença MIT
├── main.py                             # Composition Root & Injeção de Dependências
├── requirements.txt                    # Dependências de produção
├── requirements-dev.txt                # Dependências de desenvolvimento e testes
└── README.md                           # Documentação Principal
```

---

## 🚀 Como Executar Localmente

### 1. Clonar o Repositório
```bash
git clone https://github.com/felipevenas/rate-limit-validator.git
cd rate-limit-validator
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a Aplicação
```bash
python main.py
```

### 4. Executar os Testes Automatizados
```bash
python -m unittest discover tests
```

### 5. Compilar o Executável Localmente
```bash
python scripts/build_executavel.py
```
O executável final será gerado em `dist/ValidadorRateLimit.exe`.

---

## 🤝 Governança e Comunidade

- **[Guia de Contribuição](CONTRIBUTING.md)**: Convenções de commits, branches e fluxo de PRs.
- **[Código de Conduta](CODE_OF_CONDUCT.md)**: Diretrizes de respeito e convivência.
- **[Política de Segurança](SECURITY.md)**: Divulgação responsável de vulnerabilidades.
- **[Changelog](CHANGELOG.md)**: Histórico detalhado de todas as versões.

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.

<div align="center">
Desenvolvido com excelência por <b><a href="https://github.com/felipevenas">Felipe Venas</a></b>
</div>
