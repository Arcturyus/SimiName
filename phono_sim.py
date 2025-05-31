#%%
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import phonex

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

### Phonex = soundex adapté au français

def most_similar_names(nom, list_names, top_n=10, function_similarity=phonex.phonex):

    nom_reference = nom.strip()
    valeur_reference = function_similarity(nom_reference)

    distances = []
    for nom_candidat in list_names:
        nom_candidat_clean = nom_candidat.strip() if nom_candidat else ""

        valeur_candidat = function_similarity(nom_candidat_clean)
        distance = abs(valeur_reference - valeur_candidat)
        distances.append((nom_candidat_clean, distance))
            
    
    distances.sort(key=lambda x: x[1])
    
    df_results = pd.DataFrame(distances, columns=['name', 'distance'])
    return df_results[:top_n]
    
most_similar_names('ROMAIN', top_n=20, list_names=all_names)

