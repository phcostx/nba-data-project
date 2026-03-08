#%%

import pandas as pd

arquivos = [
    'PlayerStatistics.csv',
    'TeamStatistics.csv',
    'Games.csv',
    'Players.csv',
    'TeamHistories.csv',
    'LeagueSchedule24_25.csv'
]

for arquivo in arquivos:
    df = pd.read_csv(f'../data/raw/{arquivo}')
    print(f"\n{'='*50}")
    print(f"{arquivo}")
    print(f"Shape: {df.shape}")
    print(f"\nColunas:\n{df.dtypes}")
    print(f"\nNulos:\n{df.isnull().sum()}")
    print(f"\nAmostra:\n{df.head(3)}")

# %%
