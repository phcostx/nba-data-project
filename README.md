# NBA Data Project

Análise histórica de dados da NBA com foco em responder perguntas relevantes sobre performance de jogadores, times e padrões de campeões ao longo das temporadas.

---

## Objetivo

Explorar um dataset histórico da NBA para identificar padrões que diferenciam times campeões, entender a evolução do estilo de jogo ao longo das décadas e comparar performance ofensiva e defensiva entre franquias.

---

## Perguntas que o projeto responde

- Quais jogadores tiveram as maiores médias de pontos por temporada na história da NBA?
- O maior pontuador de uma temporada costuma estar no time campeão?
- Times jogando em casa têm vantagem real de aproveitamento?
- Como o volume de arremessos de 3 pontos evoluiu desde 1980?
- Os times campeões tendem a ser mais ofensivos, defensivos ou equilibrados?

---

## Dataset

Fonte: [Historical NBA Data and Player Box Scores — Kaggle](https://www.kaggle.com/datasets/eoinamoore/historical-nba-data-and-player-box-scores)

Arquivos utilizados:

| Arquivo | Descrição | Linhas |
|---|---|---|
| PlayerStatistics.csv | Box score individual por jogo | 1.6M |
| TeamStatistics.csv | Box score por time por jogo | 144K |
| Games.csv | Resultados de todas as partidas | 72K |
| Players.csv | Dados biográficos dos jogadores | 6.6K |
| TeamHistories.csv | Histórico de franquias e relocações | 140 |

---

## Stack

- **Python 3** — linguagem principal
- **Pandas** — manipulação e transformação de dados
- **SQLite** — armazenamento e modelagem relacional
- **SQLAlchemy** — ingestão dos CSVs no banco
- **Matplotlib** — visualizações exploratórias
- **Tableau Public** — dashboard interativo
- **Jupyter / VS Code Interactive** — desenvolvimento dos notebooks
- **Git + GitHub** — versionamento

---

## Estrutura do projeto

```
nba-data-project/
│
├── data/
│   ├── raw/                  # CSVs originais do Kaggle
│   └── processed/            # Dados tratados e exportados para o Tableau
│
├── notebooks/
│   ├── 01_exploracao.py      # Análise inicial — shape, dtypes, nulos
│   ├── 02_analises_sql.py    # Queries analíticas e window functions
│   └── 03_visualizacoes.py   # Gráficos com Matplotlib
│
├── sql/
│   └── create_tables.sql     # Schema do banco de dados
│
├── scripts/
│   └── load_data.py          # Ingestão dos CSVs no SQLite
│
└── README.md
```

---

## Modelagem do banco

O banco foi modelado seguindo um esquema estrela com `player_statistics` e `team_statistics` como tabelas fato, relacionadas às dimensões `players`, `games` e `team_histories` via `personId`, `gameId` e `teamId`.

---

## Análises realizadas

**SQL**
- Ranking de jogadores por média de pontos por temporada com `RANK() OVER (PARTITION BY season_year)`
- Comparativo de aproveitamento em casa vs. fora por time e temporada
- Evolução do volume de arremessos de 3 pontos desde 1980
- Cruzamento entre maior pontuador da temporada e time campeão
- Índice ofensivo e defensivo por time com window functions (`RANK`, `LAG`)

**Pandas + Matplotlib**
- Top 15 maiores pontuadores históricos
- Evolução das tentativas e conversões de 3 pontos (1980–2025)
- Aproveitamento casa vs. fora dos top 15 times em 2025
- Scatter plot do perfil ofensivo vs. defensivo dos campeões por quadrante

---

## Principais insights

- Em 45 temporadas analisadas, o maior pontuador jogava no time campeão em apenas 11 delas — menos de 25% das vezes
- Os únicos times campeões com rank 1 tanto no ataque quanto na defesa foram os Golden State Warriors de 2015 e 2017
- O Cleveland Cavaliers campeão de 2016 tinha rank defensivo 24 — LeBron James ganhou praticamente na força bruta ofensiva
- O Detroit Pistons de 2004 venceu com rank ofensivo 27 e defensivo 1 — o caso mais extremo de defesa pura na história recente
- O volume de arremessos de 3 pontos cresceu 15x desde 1980, de 2.5 para 37.3 tentativas por jogo

---

## Dashboard

[Tableau Public](https://public.tableau.com/views/nba-data-project/Planilha2?:language=pt-BR&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
