# Descrição do Pull Request

Por favor, inclua um resumo das alterações realizadas e quais problemas ou funcionalidades foram abordados.

---

## Tipo de Alteração

- [ ] 🚀 Nova funcionalidade (`feature`)
- [ ] 🐞 Correção de bug (`bug fix`)
- [ ] 🔧 Refatoração de código sem alteração funcional (`refactor`)
- [ ] 📝 Atualização de documentação (`docs`)
- [ ] 🎨 Estilo / Design / QSS / UI (`style`, `ui`)
- [ ] ⚙️ Ajustes de infraestrutura, CI/CD ou compilação do `.exe` (`ci/cd`, `build`)

## Como foi testado?

Por favor, descreva as validações executadas para verificar suas alterações:

- [ ] **Testes Automatizados:** Executou `python -m unittest discover tests` e todos os 17+ testes passaram com 100% de sucesso.
- [ ] **Interface Gráfica Local:** Executou `python main.py` e validou a responsividade, ambos os temas (Dark/Light) e a integridade visual.
- [ ] **Bateria de Testes Real:** Disparou requisições para endpoints de teste e verificou a inserção em tempo real na tabela e nos cards de métricas.
- [ ] **Compilação do Executável:** Executou `python scripts/build_executavel.py` e gerou o arquivo `.exe` funcional sem warnings críticos.

## Evidência Visual / Layout

*Cole capturas de tela ou GIFs da interface com as modificações ou logs significativos do terminal.*

## Checklist de Qualidade

- [ ] Meu código segue as diretrizes de Clean Architecture e SOLID do projeto.
- [ ] Realizei uma auto-revisão detalhada do meu próprio código.
- [ ] Não inseri estilos inline rígidos nos widgets Python (centralizados em `tema.py`).
- [ ] Adicionei/atualizei testes unitários para cobrir as novas regras de negócio.
- [ ] Atualizei a documentação e o `CHANGELOG.md` conforme necessário.
