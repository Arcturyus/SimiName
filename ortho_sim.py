#%%
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import Levenshtein


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

def freq_letter(word):
    """
    Calculate the frequency of each letter in a word.
    """
    
    letter_to_index = {chr(i + ord('a')): i for i in range(26)}
    
    # Initialize frequency array
    freq = [0] * 26
    for letter in word:
        if letter in letter_to_index:
            freq[letter_to_index[letter]] += 1
    
    return freq

def ngram_letter(word, n):
    """
    Calculate the n-gram frequency of letters in a word.
    """
    letter_to_index = {chr(i + ord('a')): i for i in range(26)}
    
    # Initialize n-gram frequency array
    ngram_freq = [0] * (26 ** n)
    
    # Generate n-grams
    for i in range(len(word) - n + 1):
        ngram = word[i:i+n]
        if all(letter in letter_to_index for letter in ngram):
            index = sum(letter_to_index[letter] * (26 ** (n - j - 1)) for j, letter in enumerate(ngram))
            ngram_freq[index] += 1
    
    return ngram_freq

len(freq_letter('alice')),len(ngram_letter('alice', 2))
#%%


def most_similar_names(nom, top_n=10,list_names=[],function_letter=freq_letter):

    similarities = []
    vec_nom = function_letter(nom.lower())
    for other_nom in list_names:
        if other_nom != nom:
            details = cosine_similarity([vec_nom], [function_letter(other_nom.lower())])[0][0]
            result_entry = {
                'nom1': nom,
                'nom2': other_nom,
                'score_final': details
            }
            similarities.append(result_entry)

    # Convert results to a DataFrame for easier viewing/sorting
    results_df = pd.DataFrame(similarities)
    
    return results_df.sort_values(by='score_final', ascending=False).head(top_n)

df_freqletter = most_similar_names('ROMAIN', top_n=200, list_names=all_names)
df_2grams = most_similar_names('ROMAIN', top_n=200, list_names=all_names, function_letter=lambda x: ngram_letter(x, 2))

df_merged = pd.merge(df_freqletter, df_2grams, on='nom2', suffixes=('_freq', '_2gram'))
df_merged = df_merged[['nom2', 'score_final_freq', 'score_final_2gram']]
df_merged['score_sum'] = df_merged['score_final_freq'] + df_merged['score_final_2gram']
df_merged = df_merged.sort_values(by='score_sum', ascending=False)
df_merged


#%%
def most_similar_names_distance(nom, top_n=10, list_names=[], function_distance=Levenshtein.distance,inverse=False):
    similarities = []
    for other_nom in list_names:
        if other_nom != nom:
            distance = function_distance(nom.lower(), other_nom.lower())
            result_entry = {
                'nom1': nom,
                'nom2': other_nom,
                'distance': distance
            }
            similarities.append(result_entry)
    results_df = pd.DataFrame(similarities)
    if inverse:
        return results_df.sort_values(by='distance', ascending=False).head(top_n)
    else:
        return results_df.sort_values(by='distance').head(top_n)

# Test with all 4 distance functions
df_distance = most_similar_names_distance('ROMAIN', top_n=200, list_names=all_names, function_distance=Levenshtein.distance)
df_ratio = most_similar_names_distance('ROMAIN', top_n=200, list_names=all_names, function_distance=Levenshtein.ratio, inverse=True)
df_jaro = most_similar_names_distance('ROMAIN', top_n=200, list_names=all_names, function_distance=Levenshtein.jaro, inverse=True)
df_jaro_winkler = most_similar_names_distance('ROMAIN', top_n=200, list_names=all_names, function_distance=Levenshtein.jaro_winkler, inverse=True)

# Merge all distance/similarity results
df_all = df_distance[['nom2', 'distance']].rename(columns={'distance': 'levenshtein_distance'})
df_all = df_all.merge(df_ratio[['nom2', 'distance']].rename(columns={'distance': 'ratio'}), on='nom2')
df_all = df_all.merge(df_jaro[['nom2', 'distance']].rename(columns={'distance': 'jaro'}), on='nom2')
df_all = df_all.merge(df_jaro_winkler[['nom2', 'distance']].rename(columns={'distance': 'jaro_winkler'}), on='nom2')

# Also merge with the frequency/ngram results
df_all = df_all.sort_values(by='jaro_winkler', ascending=False)
df_all