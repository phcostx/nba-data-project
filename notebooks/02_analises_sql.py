# %%

import sqlite3
import pandas as pd

conn = sqlite3.connect('../data/nba.db')

#%%
query = """
SELECT
    ps.firstName || ' ' || ps.lastName  AS player,
    SUBSTR(ps.gameDateTimeEst, 1, 4)    AS season_year,
    COUNT(ps.gameId)                    AS games_played,
    ROUND(AVG(ps.points), 1)            AS avg_points,
    ROUND(AVG(ps.assists), 1)           AS avg_assists,
    ROUND(AVG(ps.reboundsTotal), 1)     AS avg_rebounds
FROM player_statistics ps
WHERE ps.points IS NOT NULL
GROUP BY player, season_year
HAVING games_played >= 60
ORDER BY avg_points DESC
LIMIT 50
"""

df_alltime = pd.read_sql_query(query, conn)
df_alltime.head(50)

#%%

query = """
SELECT
    ts.teamCity || ' ' || ts.teamName AS team,
    SUBSTR(ts.gameDateTimeEst, 1, 4)  AS season_year,
    COUNT(CASE WHEN ts.home = 1 THEN 1 END)                         AS home_games,
    COUNT(CASE WHEN ts.home = 0 THEN 1 END)                         AS away_games,
    ROUND(AVG(CASE WHEN ts.home = 1 THEN ts.win END) * 100, 1)      AS home_win_pct,
    ROUND(AVG(CASE WHEN ts.home = 0 THEN ts.win END) * 100, 1)      AS away_win_pct,
    ROUND(AVG(CASE WHEN ts.home = 1 THEN ts.teamScore END), 1)      AS home_avg_score,
    ROUND(AVG(CASE WHEN ts.home = 0 THEN ts.teamScore END), 1)      AS away_avg_score
FROM team_statistics ts
WHERE ts.teamScore IS NOT NULL
GROUP BY team, season_year
HAVING home_games >= 10
ORDER BY season_year DESC, home_win_pct DESC
"""

df_home_away = pd.read_sql_query(query, conn)
df_home_away.head(20)   
# %%

query = """
SELECT
    SUBSTR(ts.gameDateTimeEst, 1, 4)         AS season_year,
    COUNT(DISTINCT ts.gameId)                AS total_games,
    ROUND(AVG(ts.threePointersAttempted), 1) AS avg_3pt_attempted,
    ROUND(AVG(ts.threePointersMade), 1)      AS avg_3pt_made,
    ROUND(AVG(ts.threePointersPercentage) * 100, 1) AS avg_3pt_pct
FROM team_statistics ts
WHERE ts.threePointersAttempted IS NOT NULL
  AND ts.threePointersAttempted > 0
  AND SUBSTR(ts.gameDateTimeEst, 1, 4) >= '1980'
GROUP BY season_year
ORDER BY season_year ASC
"""

df_three = pd.read_sql_query(query, conn)
df_three

# %%

campeoes = {
    1980: 'Los Angeles Lakers', 1981: 'Boston Celtics', 1982: 'Los Angeles Lakers',
    1983: 'Philadelphia 76ers', 1984: 'Boston Celtics', 1985: 'Los Angeles Lakers',
    1986: 'Boston Celtics', 1987: 'Los Angeles Lakers', 1988: 'Los Angeles Lakers',
    1989: 'Detroit Pistons', 1990: 'Detroit Pistons', 1991: 'Chicago Bulls',
    1992: 'Chicago Bulls', 1993: 'Chicago Bulls', 1994: 'Houston Rockets',
    1995: 'Houston Rockets', 1996: 'Chicago Bulls', 1997: 'Chicago Bulls',
    1998: 'Chicago Bulls', 1999: 'San Antonio Spurs', 2000: 'Los Angeles Lakers',
    2001: 'Los Angeles Lakers', 2002: 'Los Angeles Lakers', 2003: 'San Antonio Spurs',
    2004: 'Detroit Pistons', 2005: 'San Antonio Spurs', 2006: 'Miami Heat',
    2007: 'San Antonio Spurs', 2008: 'Boston Celtics', 2009: 'Los Angeles Lakers',
    2010: 'Los Angeles Lakers', 2011: 'Dallas Mavericks', 2012: 'Miami Heat',
    2013: 'Miami Heat', 2014: 'San Antonio Spurs', 2015: 'Golden State Warriors',
    2016: 'Cleveland Cavaliers', 2017: 'Golden State Warriors', 2018: 'Golden State Warriors',
    2019: 'Toronto Raptors', 2020: 'Los Angeles Lakers', 2021: 'Milwaukee Bucks',
    2022: 'Golden State Warriors', 2023: 'Denver Nuggets', 2024: 'Boston Celtics'
}

df_campeoes = pd.DataFrame([
    {'season_year': str(ano), 'champion': time}
    for ano, time in campeoes.items()
])

query = """
SELECT
    SUBSTR(ps.gameDateTimeEst, 1, 4)    AS season_year,
    ps.firstName || ' ' || ps.lastName  AS top_scorer,
    ps.playerteamCity || ' ' || ps.playerteamName AS team,
    COUNT(ps.gameId)                    AS games_played,
    ROUND(AVG(ps.points), 1)            AS avg_points
FROM player_statistics ps
WHERE ps.points IS NOT NULL
GROUP BY season_year, top_scorer, team
HAVING games_played >= 60
ORDER BY season_year, avg_points DESC
"""

df_scorers = pd.read_sql_query(query, conn)

df_top = df_scorers.groupby('season_year').first().reset_index()

df_final = df_top.merge(df_campeoes, on='season_year', how='inner')
df_final['scorer_is_champion'] = df_final.apply(
    lambda r: 'Sim' if r['champion'].lower() in r['team'].lower() else 'Não', axis=1
)

df_final[['season_year', 'top_scorer', 'team', 'avg_points', 'champion', 'scorer_is_champion']]

#%%

df_final.to_csv('../data/processed/top_scorer_vs_champion.csv', index=False)
df_home_away.to_csv('../data/processed/home_away_performance.csv', index=False)
df_three.to_csv('../data/processed/three_point_evolution.csv', index=False)
df_alltime.to_csv('../data/processed/player_avg_points_alltime.csv', index=False)

print("Arquivos salvos em data/processed/")