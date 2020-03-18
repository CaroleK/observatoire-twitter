# Observatoire Twitter

## 1. Objectif du projet
Développer deux cas d'usage d'utilisation des données Twitter pour les entreprises.

Les données sont récoltées par scrapping, et analysées par nos algorithmes.

## 2. Organisation
Le projet est découpé en 3 dossiers :
* **data**: contient les scripts d'extraction des données et les données (non disponibles sur github)
* **source**: contient les modèles de traitement des données finalisés
* **test**: contient les notebooks et les scripts utiles pour le développement

## 3. Mode d'emploi

### Extraction des données
Nous utilisons la librairie Twint pour extraire des données via scrapping.
Cela se fait en exécutant le script `data/extraction_twint/extraction_tweets`.
Deux fonction sont appelées, correspondant aux deux cas d'usages choisis (service clients et marketing personnalisé), et il est possible de paramètrer le nombre maximum de tweets à extraire.

### Calcul du temps de réponse
Pour le cas d'usage **Service clients**, il est nécessaire de calculer les temps de réponse des marques aux tweets les mentionnant.
Il faut exécuter le script `data/extraction_twint/reply_time` pour réaliser cette opération.

### Extraction des données de comptes twitter
Il est aussi possible de compléter des datasets de tweets avec toutes les informations du compte ayant publié le tweet, pour cela il faut exécuter deux scripts :
- `data/extraction_twint/user_info` qui réalise l'extraction des données de tous les comptes
- `data/extraction_twint/join_tweets_user_info` qui réalise la jointure entre la base de données de tweets et celle extraite par le script précédent



