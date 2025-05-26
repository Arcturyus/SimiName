#%%
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

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
##### TODO ET UN QUI STOCKE LES ALL NAMES DONNER PLUS DE X FOIS DEPUIS 1900

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

freq_letter('alice')
#%%


def most_similar_names(nom, top_n=10,list_names=[]):

    similarities = []
    vec_nom = freq_letter(nom.lower())
    for other_nom in list_names:
        if other_nom != nom:
            # Store the results along with the names
            details = cosine_similarity([vec_nom], [freq_letter(other_nom.lower())])[0][0]
            result_entry = {
                'nom1': nom,
                'nom2': other_nom,
                'score_final': details # Unpack the dictionary from cos_sim_nom
            }
            similarities.append(result_entry)

    # Convert results to a DataFrame for easier viewing/sorting
    results_df = pd.DataFrame(similarities)
    
    return results_df.sort_values(by='score_final', ascending=False).head(top_n)

most_similar_names('ROMAIN', top_n=25, list_names=all_names)