#%%
import pandas as pd
import gensim.downloader as api
from gensim.models import KeyedVectors

#%%
# Read the CSV file
df = pd.read_csv('data/prenoms-2023-nat.csv', sep=';', encoding='utf-8')
# Filter to keep only rows where 'annais' is numeric
initial_count = len(df)
df = df[pd.to_numeric(df['annais'], errors='coerce').notna()]
final_count = len(df)
removed_count = initial_count - final_count
print(f"Removed {removed_count}/{initial_count} rows with non-numeric 'annais' values")
#%%
##### TODO REMPLACE CA PAR UN FICHIER QUI STOCKE LA LISTE ALL NAMES 
##### TODO ET UN QUI STOCKE LES ALL NAMES present PLUS DE X FOIS DEPUIS 1900

series_masculin = {}
series_feminin = {}

df_m = df[df['sexe'] == 1]
df_f = df[df['sexe'] == 2]

for prenom, group in df_m.groupby('preusuel'):
    series_masculin[prenom.lower()] = group.set_index(group['annais'].astype(int))['nombre'].astype(int).sort_index()

for prenom, group in df_f.groupby('preusuel'):
    series_feminin[prenom.lower()] = group.set_index(group['annais'].astype(int))['nombre'].astype(int).sort_index()
all_names = list(set(series_masculin.keys()) | set(series_feminin.keys()))

#%%

