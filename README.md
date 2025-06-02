# SimiName

1. Courbes d’usage (INSEE, SSA…) : deux prénoms en vogue à la même époque se rapprochent.
Data : https://www.insee.fr/fr/statistiques/8205621


2. Représentations par embeddings de mots
On traite chaque prénom comme un “mot” : on peut entraîner (ou utiliser) un modèle Word2Vec/GloVe sur un corpus (ex. Wikipedia) et extraire un vecteur.
Deux prénoms apparaissant dans des contextes similaires (articles, listes) partageront des vecteurs proches.

3. Similarité orthographique
Fréquence Lettres et N-grammes
    - **Fréquence de lettres** : compte des occurrences de chaque lettre dans les prénoms.
      - Exemple : "Anna" → [2, 0, ..., 2, ...] (pour a-z).
    - **N-grammes de lettres** : séquences de 2, 3 lettres (bi-grammes, tri-grammes) pour capturer les motifs communs.
    - **One-hot encoding** : chaque prénom devient un vecteur binaire indiquant la présence/absence de chaque lettre.
     - Exemple : "Alice" → [...] pour aa, ab, ac, ..., zz. (taille 676 pour 2-grammes)

Peut être combiné avec réduction de dimension (PCA/t-SNE/UMAP) pour visualisation ou clustering.

    - **Distance d'édition (Levenshtein)** : opérations minimum entre deux prénoms
    - **Jaro-Winkler** : pondère davantage les débuts de chaînes
    

5. Similarité phonétique
    - Algorithmes Soundex/Metaphone : rapprochent par prononciation (phonex librairie adapté au français)
    - Distance sur transcriptions IPA : mesure entre représentations phonétiques

6. ou info dessus (sens, origine, etc.) ?

## Sites

L'idée c'est d'en faire un petit site avec plusieurs fonctionnalités :

**Recherche de prénoms similaires**  
- Saisie d'un prénom et récupération automatique des prénoms similaires via différentes techniques (embeddings, distances d'édition, phonétiques, etc.).  
- Suggestion et comparaison des prénoms en se basant sur des critères multiples.

**Visualisation des courbes d'usage (1900-2023)**  
- Affichage interactif d'une courbe de popularité du prénom sélectionné sur la période 1900-2023.  
- Comparaison en temps réel des tendances d'usage entre le prénom donné et ses prénoms similaires.

**Analyses complémentaires**  
- Exploration des similarités orthographiques et statistiques à travers des graphiques détaillés.  
- Options de filtrage et de personnalisation (par exemple par genre, date min, max, ... ou par autre critère qu'on a ou mettre des poids sur les critères de similarité).


