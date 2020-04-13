# Observatoire Twitter

## 1. Objectif du projet
Développer deux cas d'usage d'utilisation des données Twitter pour les entreprises.

Les données sont récoltées par scrapping, et analysées par nos algorithmes.

## 2. Organisation
Le projet est découpé en 3 dossiers :
* **data**: contient les scripts d'extraction des données et les données (non disponibles sur github)
* **source**: contient les modèles de traitement des données finalisés
* **test**: contient les notebooks et les scripts utiles pour le développement

```
.
├── data                                              << Scripts d'extractions de données et données
│   ├── extraction_manual                             <== 1ère version des scripts d'extraction
│   │   ├── data_treatment.py
│   │   ├── __main__.py
│   │   ├── product_keywords.xlsx
│   │   ├── tweets_collection.py
│   │   └── user_tweets.py
│   └── extraction_twint                              <== Extraction via twint
│       ├── brand_accounts.csv                        <-- liste des comptes à extraire pour le cas d'usage service clients
│       ├── extraction_tweets.py                      <-- script d'extraction des tweets
│       ├── join_tweets_user_info.py                  <-- script ajoutant les données d'utilisateurs aux tweets
│       ├── product_keywords.csv                      <-- liste des produits à extraire pour la cas d'usage marketing
│       ├── reply_time_notebook_version.ipynb
│       ├── reply_time.py                             <-- script calculant les temps de réponses de la marque
│       ├── tweets_data                               <-- données extraites (non disponible sur Github)
│       │   ├── data_marketing_personnalise           
│       │   │   ├── pepsi.csv
│       │   │   └── pepsi_users.csv
│       │   └── data_service_clients
│       │       ├── embeddings                        <-- stockage des tweets après embedding
│       │       │   ├── GloveTwitter200d
│       │       │   │   └── amazon.csv
│       │       │   └── GoogleVectors300d
│       │       │       └── amazon.csv
│       │       ├── raw                               <-- tweets bruts
│       │       │   └── amazon.csv
│       │       ├── users_info                        <-- données utilisateurs des auteurs des tweets du dossier raw
│       │       │   └── amazon.csv
│       │       ├── with_reply_time                   <-- données brutes avec reply_time
│       │       │   └── amazon.csv
│       │       └── with_user_info                    <-- données brutes avec reply_time et données utilisateur
│       │           └── amazon.csv
│       └── user_info.py                              <-- script d'extractions des données d'utilisateurs
├── README.md
├── source                                            << modèles de traitement des données
│   ├── embeddings                                    <== modèles d'embeddings (non disponible sur GitHub)
│   │   ├── GloveTwitter200d                          <-- Modèle GloVe
│   │   │   └── glove.twitter.27B.200d.txt
│   │   └── GoogleVectors300d                         <-- Modèle Google Word2Vec
│   │       └── GoogleNews-vectors-negative300.bin
│   ├── emoticons.py                                  <-- script de traitement des emoticones
│   ├── __init__.py
│   ├── preprocessing.py                              <-- script contenant des fonctions de prétraitement
│   └── slang.txt                                     <-- dictionnaire d'abréviations
└── tests                                             << Notebooks utilisés pour le développement des cas d'usage
    ├── marketing_personnalise                       
    │   └── NameEntityRecognition.ipynb
    └── service_client
        └── Service Client.ipynb
```


## 3. Mode d'emploi

### Génération des données
#### Extraction des tweets
Nous utilisons la librairie Twint pour extraire des données via scrapping.
Cela se fait en exécutant le script `data/extraction_twint/extraction_tweets`.
Deux fonction sont appelées, correspondant aux deux cas d'usages choisis (service clients et marketing personnalisé), et il est possible de paramètrer le nombre maximum de tweets à extraire.

#### Calcul du temps de réponse
Pour le cas d'usage **Service clients**, il est nécessaire de calculer les temps de réponse des marques aux tweets les mentionnant.
Il faut exécuter le script `data/extraction_twint/reply_time` pour réaliser cette opération.

#### Extraction des données de comptes twitter
Il est aussi possible de compléter des datasets de tweets avec toutes les informations du compte ayant publié le tweet, pour cela il faut exécuter deux scripts :
- `data/extraction_twint/user_info` qui réalise l'extraction des données de tous les comptes
- `data/extraction_twint/join_tweets_user_info` qui réalise la jointure entre la base de données de tweets et celle extraite par le script précédent

### Cas d'usages

#### Cas d'usage Marketing personnalisé
Le code que nous avons utilisé pour obtenir nos résultats sur ce cas d'usage est contenu dans le notebook `tests/marketing_personnalise/NameEntityRecognition.ipynb`

#### Cas d'usage Services clients
Le code que nous avons utilisé pour obtenir nos résultats sur ce cas d'usage est contenu dans le notebook `tests/service_client/Service Client.ipynb`



