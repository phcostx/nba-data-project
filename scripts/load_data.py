import pandas as pd
import sqlite3

conn = sqlite3.connect('data/nba.db')

# Executa o schema
with open('sql/create_tables.sql', 'r') as f:
    conn.executescript(f.read())

# Players
players = pd.read_csv('data/raw/Players.csv')
players.to_sql('players', conn, if_exists='replace', index=False)
print("players OK")

# Team Histories
teams = pd.read_csv('data/raw/TeamHistories.csv')
teams.to_sql('team_histories', conn, if_exists='replace', index=False)
print("team_histories OK")

# Games
games = pd.read_csv('data/raw/Games.csv')
games = games[['gameId','gameDateTimeEst','hometeamCity','hometeamName',
               'hometeamId','awayteamCity','awayteamName','awayteamId',
               'homeScore','awayScore','winner','gameType','attendance']]
games.to_sql('games', conn, if_exists='replace', index=False)
print("games OK")

# Player Statistics
ps = pd.read_csv('data/raw/PlayerStatistics.csv', low_memory=False)
ps = ps.rename(columns={'personId': 'personId'})
ps.to_sql('player_statistics', conn, if_exists='replace', index=False)
print("player_statistics OK")

# Team Statistics
ts = pd.read_csv('data/raw/TeamStatistics.csv')
ts.to_sql('team_statistics', conn, if_exists='replace', index=False)
print("team_statistics OK")

conn.close()
print("\nBanco criado com sucesso em data/nba.db")