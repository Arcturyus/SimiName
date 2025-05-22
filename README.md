# SimiName

1. 
Courbes d’usage (INSEE, SSA…) : deux prénoms en vogue à la même époque se rapprochent.

2. Représentations par embeddings de mots
On traite chaque prénom comme un “mot” : on peut entraîner (ou utiliser) un modèle Word2Vec/GloVe sur un corpus (ex. Wikipedia) et extraire un vecteur.
Deux prénoms apparaissant dans des contextes similaires (articles, listes) partageront des vecteurs proches.

3. Lettres
One-hot sur lettres + réduction de dimension
Chaque prénom → vecteur binaire de présence/occurrence de chaque lettre (26 dimensions), qu’on réduit ensuite via PCA/t-SNE/UMAP ?

4. Similarité orthographique
    - Distance d'édition (Levenshtein) : opérations minimum entre deux prénoms
    - Jaro-Winkler : pondère davantage les débuts de chaînes
    - N-grammes de caractères : chevauchement de séquences de lettres

5. Similarité phonétique
    - Algorithmes Soundex/Metaphone : rapprochent par prononciation
    - Distance sur transcriptions IPA : mesure entre représentations phonétiques

6. ou info dessus (sens, origine, etc.) ?