# Guia de Contribuição 🤝

Agradecemos o seu interesse em contribuir para o **Rate Limit Validator & Stress Tester**! Este documento orienta o processo de desenvolvimento e os padrões adotados para manter o código limpo, modular e seguro.

---

## 🛠️ Ambiente de Desenvolvimento

### 1. Clonar o Repositório
```bash
git clone https://github.com/felipevenas/rate-limit-validator.git
cd rate-limit-validator
```

### 2. Criar e Ativar um Ambiente Virtual
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências de Desenvolvimento
```bash
pip install -r requirements-dev.txt
```

---

## 🌿 Fluxo de Branches e Commits

Adotamos a convenção de **Git Flow** e **Conventional Commits**:

### Nomes de Branches
- `feature/<nome-da-funcionalidade>` (ex: `feature/exportacao-pdf`)
- `fix/<nome-do-bug>` (ex: `fix/ordenacao-tabela`)
- `docs/<nome-do-documento>` (ex: `docs/atualiza-readme`)
- `refactor/<nome-do-modulo>` (ex: `refactor/camada-dominio`)

### Padrão de Mensagens de Commit
- `feat: adiciona suporte a exportação de relatórios em formato JSON`
- `fix: corrige índice de linha na inserção em tempo real`
- `docs: adiciona guia de contribuição e governança`
- `style: refina bordas e contraste do tema escuro`
- `test: adiciona testes unitários para o parse de cabeçalhos de rate limit`

---

## 🏛️ Diretrizes Arquiteturais

1. **Clean Architecture e SOLID**:
   - Mantenha a camada de `domain/` 100% pura, sem dependências de frameworks.
   - Respeite o **SRP (Princípio da Responsabilidade Única)**.
2. **Estilização em PySide6 / Qt**:
   - Não insira estilos inline nos construtores Python. Todas as regras de design devem ser centralizadas em `src/presentation/styles/tema.py` com seletores semânticos para suportar tanto o Dark Mode quanto o Light Mode.
3. **Testes Unitários**:
   - Todo novo recurso ou correção de bug deve vir acompanhado de testes unitários em `tests/`.

---

## 🧪 Como Rodar os Testes e Compilar

### Rodar a Suíte de Testes
```bash
python -m unittest discover tests
```

### Compilar o Executável (.exe)
```bash
python scripts/build_executavel.py
```

---

## 📬 Submetendo um Pull Request

1. Crie uma branch a partir de `main` ou `develop`.
2. Realize suas modificações mantendo os testes 100% verdes.
3. Atualize o `CHANGELOG.md` com suas adições.
4. Abra o Pull Request preenchendo o template oficial com evidências e passos de teste.
