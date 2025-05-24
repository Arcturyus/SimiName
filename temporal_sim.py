#%%
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
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
series_masculin = {}
series_feminin = {}

df_m = df[df['sexe'] == 1]
df_f = df[df['sexe'] == 2]

for prenom, group in df_m.groupby('preusuel'):
    series_masculin[prenom] = group.set_index(group['annais'].astype(int))['nombre'].astype(int).sort_index()

for prenom, group in df_f.groupby('preusuel'):
    series_feminin[prenom] = group.set_index(group['annais'].astype(int))['nombre'].astype(int).sort_index()

#%%
def plot_prenom(nom, series_masculin, series_feminin, figsize=(12, 6)):
    """
    Plot les séries en subplots côte à côte avec des échelles Y indépendantes
    et une échelle X commune de 1900 à 2023.
    """
    serie_m = series_masculin.get(nom)
    serie_f = series_feminin.get(nom)

    # Vérifier si au moins une des séries contient des données
    has_data_m = serie_m is not None and not serie_m.empty
    has_data_f = serie_f is not None and not serie_f.empty

    if not has_data_m and not has_data_f:
        print(f"Aucune donnée trouvée pour le prénom '{nom}'")
        return
    
    

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    # Plot masculin
    if has_data_m:
        if len(serie_m) < 20:
            axes[0].plot(serie_m.index, serie_m.values, marker='o', color='steelblue', linewidth=0, markersize=6, label='Masculin')
        else:
            axes[0].plot(serie_m.index, serie_m.values, marker='o', color='steelblue', linewidth=2, label='Masculin')
    axes[0].set_title(f'{nom} - Masculin')
    axes[0].grid(True, alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)

    # Plot féminin
    if has_data_f:
        if len(serie_f) < 20:
            axes[1].plot(serie_f.index, serie_f.values, marker='o', color='pink', linewidth=0, markersize=6, label='Féminin')
        else:
            axes[1].plot(serie_f.index, serie_f.values, marker='o', color='pink', linewidth=2, label='Féminin')
    axes[1].set_title(f'{nom} - Féminin')
    axes[1].grid(True, alpha=0.3)
    axes[1].tick_params(axis='x', rotation=45)

    # Fixe le bas à 0 pour les deux axes
    axes[0].set_ylim(bottom=0)
    axes[1].set_ylim(bottom=0)
    # Fixe l'échelle X de 1900 à 2023 pour les deux axes
    axes[0].set_xlim(1900, 2023)
    axes[1].set_xlim(1900, 2023)

    plt.tight_layout()
    plt.show()

    fig.suptitle(f'Évolution du prénom "{nom}" (1900-2023)', fontsize=16, fontweight='bold')

    
    plt.tight_layout(rect=[0, 0, 1, 0.97]) # Ajuster pour le suptitle
    plt.show()

    # Afficher quelques statistiques
    print(f"\n=== Statistiques pour {nom} ===")
    if has_data_m:
        print(f"Masculin - Total: {serie_m.sum():,} | Année Pic: {serie_m.idxmax()} ({serie_m.max():,}) | Moyenne: {serie_m.mean():.0f}")
    if has_data_f:
        print(f"Féminin  - Total: {serie_f.sum():,} | Année Pic: {serie_f.idxmax()} ({serie_f.max():,}) | Moyenne: {serie_f.mean():.0f}")
plot_prenom('ROMAIN', series_masculin, series_feminin)
# %%
# cos sim
def cos_sim_nom(nom1,nom2):
    serie_m1 = series_masculin.get(nom1)
    serie_f1 = series_feminin.get(nom1)
    serie_m2 = series_masculin.get(nom2)
    serie_f2 = series_feminin.get(nom2)
    

    years = range(1900, 2024)
    
    # Convert to vectors with 0 for missing years
    def series_to_vector(serie, years):
        if serie is None or serie.empty:
            return np.zeros(len(years))
        vector = []
        for year in years:
            vector.append(serie.get(year, 0))
        return np.array(vector)
    
    # Convert all series to vectors
    vec_m1 = series_to_vector(serie_m1, years)
    vec_f1 = series_to_vector(serie_f1, years)
    vec_m2 = series_to_vector(serie_m2, years)
    vec_f2 = series_to_vector(serie_f2, years)
    
    # Calculate cosine similarities
    cos_sim_m = cosine_similarity([vec_m1], [vec_m2])[0][0]
    cos_sim_f = cosine_similarity([vec_f1], [vec_f2])[0][0]
    

    norm_m1 = np.linalg.norm(vec_m1)
    norm_m2 = np.linalg.norm(vec_m2)
    norm_f1 = np.linalg.norm(vec_f1)
    norm_f2 = np.linalg.norm(vec_f2)
    
    # Normes moyennes pour chaque paire
    norm_m_avg = (norm_m1 + norm_m2) / 2
    norm_f_avg = (norm_f1 + norm_f2) / 2
    
    # Normalisation des poids (pour que la somme = 1)
    total_norm = norm_m_avg + norm_f_avg
    weight_m = norm_m_avg / total_norm
    weight_f = norm_f_avg / total_norm
    
    score_final = weight_m * cos_sim_m + weight_f * cos_sim_f
    details = {
        'cos_sim_m': cos_sim_m,
        'cos_sim_f': cos_sim_f,
        'norm_m_avg': norm_m_avg,
        'norm_f_avg': norm_f_avg,
        'weight_m': weight_m,
        'weight_f': weight_f,
        'score_final': score_final
    }

    return details

cos_sim_nom('ROMAIN','CHARLOTTE')

# %%
all_names = list(set(series_masculin.keys()) | set(series_feminin.keys()))
def most_similar_names(nom, top_n=10,list_names=[]):
    """
    Find the top N most similar names to the given name based on cosine similarity.
    """
    similarities = []
    
    for other_nom in list_names:
        if other_nom != nom:
            # Store the results along with the names
            details = cos_sim_nom(nom, other_nom)
            result_entry = {
                'nom1': nom,
                'nom2': other_nom,
                **details # Unpack the dictionary from cos_sim_nom
            }
            similarities.append(result_entry)

    # Convert results to a DataFrame for easier viewing/sorting
    results_df = pd.DataFrame(similarities)
    
    return results_df.sort_values(by='score_final', ascending=False).head(10)

most_similar_names('ROMAIN', top_n=10, list_names=all_names)