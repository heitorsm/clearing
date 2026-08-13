# Runbook clearing (pt-BR)

Guia operacional do plugin clearing: o que fazer em cada situação, o que digitar, o que esperar. A linguagem do plugin (comandos, status, campos) é inglês; este runbook é a camada de uso em português.

## Pré-checagem (uma vez por sessão)

1. Obsidian aberto na máquina.
2. `obsidian version` responde no terminal. Se não responder: re-registrar a CLI em Settings: General: Command line interface e abrir um terminal novo.
3. O Claude anuncia o modo na primeira operação: **vault-mode** (experiência completa) ou **artifact-mode** (sem CLI; ver UC10).

## Mapa de 10 segundos

| Situação | O que fazer | Frequência |
|---|---|---|
| Ideia solta no meio do dia | "tive uma ideia: ..." | Sempre, na hora |
| Li algo que vale guardar | Web Clipper ou "capture isso: ..." | Sempre, na hora |
| Inbox acumulou | `/triage` | Diário ou a cada 2-3 dias |
| Decisão difícil e aberta | `/diverge <problema>` | Pontos de decisão |
| O que está maduro? Rever os pontos | `/converge` | Semanal |
| O que eu pensava sobre X? | "o que eu estava pensando sobre X?" | Sob demanda |
| Ideia promovida terminou | "a ideia X funcionou/falhou porque..." | Ao concluir |
| Vault bagunçado, notas antigas | `/diagnose` e depois `/enrich` | Contínuo, em lotes |
| Visão de sistema, padrões maiores | `/emerge` | Mensal |

## Casos de uso

### UC1. Estou lendo um artigo, PDF ou blog post e quero criar uma nota no parking lot

Dois caminhos, conforme onde você está lendo:

**Caminho A: artigo na web.** Use o Obsidian Web Clipper como sempre: a nota cai em `Clippings/` com os metadados do Clipper (title, source, author). Ela entra no sistema na próxima `/triage` ou `/enrich`, que adiciona maturity, tags temáticas e connections sem tocar nos campos do Clipper.

**Caminho B: lendo com o Claude (PDF, transcrição, discussão).** Diga em linguagem natural:

> capture isso: o artigo do Bouschery sobre AI no double diamond defende que LLMs ampliam o problem space antes da convergência. Conexão possível com o nosso Decision HUB.

O que acontece: nota criada em `Inbox/` com `status: inbox` e `origin: reading`, confirmação em uma linha, e nada mais. Você volta à leitura.

Regra de ouro dos dois caminhos: **capture o seu pensamento, não só a fonte.** O link puro tem pouco valor de rede; o insight que o artigo provocou em você é o que gera conexões na triagem. Se durante a leitura surgir uma ideia própria derivada, capture como segunda nota separada: a ideia é sua, o artigo é referência, e a triagem conecta as duas.

O que NÃO fazer: categorizar, taguear ou decidir destino na captura. Isso é trabalho da triagem. Fricção na captura mata o hábito.

### UC2. Tive uma ideia no meio do trabalho

> tive uma ideia: usar circuit breaker no orquestrador de agentes do SunOS

Nota em `Inbox/`, slug com data, confirmação em uma linha. Não interrompa o que estava fazendo; a organização tem hora própria.

### UC3. Chegou a hora de organizar: triagem

Digite `/triage`. O Claude lista o Inbox, lê cada nota e propõe em bloco: categoria (`projects`, `insights`, `references`, `explore`), 3 a 5 tags reaproveitando o vocabulário existente, conexões com justificativa, e um próximo passo. Você valida item a item ou em bloco: aprovar, editar ou descartar.

Ao aprovar, cada nota recebe `status: parking-lot`, é reestruturada com o template e movida para a pasta semântica preservando wikilinks: `projects` para `Efforts/` (ou `Work/Clientes/<cliente>/` com sua confirmação), `insights` e `explore` para `Atlas/`, `references` para `Clippings/`. Descartes viram `status: discarded` com `reason` em uma linha e vão para `Archive/`: descarte consciente é feature, não falha. Log em `System/`.

Sinal de alerta: Inbox acima de 30 notas significa triagem atrasada; agende 15 minutos hoje.

### UC4. Preciso decidir algo difícil: divergência

> /diverge como manter o decisioning de NBA explicável para o time de auditoria do banco?

O que esperar, em ordem:

1. **Reframe**: 2 a 3 reformulações do problema (subir nível: por que isso importa?; descer: qual o bloqueio concreto?; molduras de Wedell-Wedellsborg). Você escolhe o enquadramento. Este passo existe porque o erro mais caro é divergir com maestria sobre a pergunta errada.
2. **Contrato de poda**: objetivo em uma frase, 2 a 4 critérios decidíveis e um anti-objetivo. Dica para critérios decidíveis: uma ideia passa ou falha neles sem debate. "Não pode exigir intervenção do usuário" é decidível; "deve ser elegante" não é.
3. **Grounding**: o Claude colhe 3 a 8 notas do vault e monta o brief (fatos, restrições, banlist de ideias que já existem), tudo com proveniência em wikilink.
4. **Divergência**: 5 branches paralelas e isoladas sob frames cognitivos, ~30 ideias.
5. **Poda qualificada**: score, clusters, armadilhas com razão mecânica, e cada corte citando o critério que o matou. Shortlist com a escolha não-óbvia marcada com ★.
6. **Persistência**: síntese em `Atlas/` e as top ideias viram notas `status: parking-lot` com `origin: divergence`, entrando no fluxo do `/converge`.

Quando NÃO usar: pergunta com resposta canônica, lookup, ou quando você mesmo escreveu "rápido", "padrão", "só me diz". Custa ~12 calls; é para decisões onde a resposta óbvia errada sai cara. Comparação: "qual índice usar nessa query?" é resposta direta; "como estruturar o modelo de pricing do produto X?" é `/diverge`.

### UC5. Quero rever os pontos: o que está maduro (convergência semanal)

Digite `/converge`. O Claude coleta tudo com `status: parking-lot` e o convergent-critic analisa três dimensões: clusters temáticos, maturidade (múltiplos backlinks, referências recentes, próximo passo claro) e decaimento (30+ dias sem toque). Para cada cluster, uma sugestão comprometida: promover, manter incubando, ou arquivar.

Você decide. Promover marca `status: active` e move para `Efforts/`. "Manter" é sempre resposta válida: incubação é o propósito do parking lot, não um defeito. Arquivar registra o motivo. Nada é descartado automaticamente. Log em `System/`.

Ritual sugerido: sexta à tarde ou domingo, 15 a 20 minutos.

### UC6. O que eu estava pensando sobre X? (revisão de incubação)

> o que eu estava pensando sobre personalização no app da MRV?

O Claude busca, lê as notas e reconstrói a cadeia em ordem cronológica: começou com A, conectou com B, última nota há N dias, incluindo outcomes de ideias já concluídas. Ao final, quatro opções: adicionar uma nota nova à cadeia, promover algo, arquivar a cadeia, ou só relembrar mesmo.

### UC7. Uma ideia promovida terminou: fechar o loop

> a ideia dos decision passports que virou projeto: funcionou, entrou no roadmap do BMG

O campo `outcome` recebe uma linha (`worked`, `failed` ou `learned` + o quê). Por que importa: o `/converge` e a revisão de incubação passam a mostrar seu histórico de acertos, e você aprende qual tipo de ideia sua costuma vingar.

### UC8. Saúde do vault: diagnóstico e enriquecimento

`/diagnose` entrega: cobertura de frontmatter e tags, órfãs, distribuição de maturidade, valores legados em português pendentes de migração (`ativo`, `projetos`, `leitura`...), fila de prioridade e métricas de grafo (candidatos a leverage point, pares de citação mútua, clusters sem MOC). Snapshot salvo em `System/`.

`/enrich 5` processa o topo da fila: para cada nota, proposta de type, maturity, tags, connections e migração de valores legados, tudo validado em bloco antes de aplicar. O alvo principal é `1. General/` (o acervo legado); notas consolidadas migram para `Atlas/` com sua aprovação, sem obrigação de mover.

Cadência: lotes de 5 a 10, duas a três vezes por semana. Nunca big-bang; o vault permanece funcional durante toda a migração.

### UC9. Visão de sistema: emergência mensal

Digite `/emerge`. O scan produz as métricas de grafo e o relation-scout aplica a lente de Meadows: **leverage points** (notas de alta centralidade cruzando domínios, com a direção de intervenção para cada uma), **loops de retroalimentação** (notas que se citam mutuamente e o que amplificam), **clusters auto-organizados** (grupos densos sem MOC, cada um com um MOC proposto como pergunta), e **domínios silenciosos** (volume sem pontes). Com sua aprovação, a síntese vira nota datada em `Atlas/` conectada a tudo que nomeou.

É o ritual que transforma o vault de pilha de notas em sistema que mostra os próprios pontos de alavancagem. Mensal, 15 minutos.

### UC10. Sem o vault: Cowork ou claude.ai (artifact-mode)

O modo é detectado e anunciado uma vez. O que funciona: `/diverge` quase completo (grounding nos documentos do projeto, saída como artefato versionado `current-divergence-<slug>.md` para você subir nos project files) e triagem ou convergência sobre um documento de inbox fornecido no contexto. O que não funciona: `vault-enrichment` (não há grafo sem vault; a skill declara e para). A degradação é sempre anunciada, nunca simulada.

## Como usar em cada etapa (squiggle e Double Diamond)

| Onde você está na squiggle | Sintoma | Ferramenta |
|---|---|---|
| Ruído: muitas frentes, tudo interessante | Abas demais, ideias soltas | Capturar tudo (UC1, UC2); nada de organizar agora |
| Preciso escolher o problema certo | "Nem sei qual é a pergunta" | `/diverge`: o Reframe força essa escolha antes de gerar respostas |
| Explorando soluções | "Qual caminho seguir?" | `/diverge` fases 1 e 2: branches + poda contra contrato |
| Preciso fechar: o que levo adiante? | Parking lot cheio, decisões paradas | `/converge` |
| Cadê o padrão maior? | Sensação de déjà vu entre projetos | `/emerge` |
| Manutenção do terreno | Notas antigas sem metadata | `/diagnose` + `/enrich` |

## Cadência sugerida

| Ritmo | Ação | Tempo |
|---|---|---|
| Ao longo do dia | Capturar (UC1, UC2) | Segundos por captura |
| 2-3x por semana | `/triage` | 10 min |
| Semanal | `/converge` | 15-20 min |
| Contínuo | `/enrich` em lotes de 5-10 | 10 min por lote |
| Mensal | `/emerge` + `/diagnose` comparativo | 15 min |
| Pontos de decisão | `/diverge` | 10-15 min de interação |

## Sinais de alerta

- Categorizando na hora da captura: fricção que mata o hábito. Capture e siga.
- `/diverge` para pergunta trivial: 12 calls para o que uma resposta direta resolvia.
- Aceitando todas as conexões sugeridas: conexão sem "importa porque" é ruído no grafo.
- Inbox acima de 30: triagem atrasada.
- Nunca descartar nada: parking lot vira aterro. O descarte consciente com `reason` é parte do método.
- Contrato de poda genérico ("deve ser bom"): poda sem critério decidível é poda não-qualificada.

## Troubleshooting rápido

- `obsidian: command not found`: re-registrar a CLI (Settings: General) e abrir terminal novo.
- `Error: Operator "status" not recognized`: busca por propriedade exige colchetes: `[status:parking-lot]`.
- Nota em subpasta não encontrada: use `path="Pasta/nota.md"`; `name=` não aceita `/`.
- Wikilinks quebrados após mover: algo usou `mv` do sistema. Sempre `obsidian move`.
- Operação em massa lenta: a CLI é uma chamada por comando; análise em escala é do `scan_vault.py`.

Referência completa de sintaxe: `references/obsidian-cli.md` dentro das skills, ou README do plugin.
