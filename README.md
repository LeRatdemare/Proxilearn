# 📚 Proxylearn - Apprentissage Adaptatif avec l'IA

Proxylearn est un projet d'intégration de l'intelligence artificielle pour la personnalisation des parcours d'apprentissage en fonction du niveau et des besoins des élèves. Il repose sur l'algorithme ZPDES (Zone Proximale de Développement et Exploration Séquentielle), inspiré des bandits multi-bras.
Il s'incrit dns le cadre d'un projet de parcours d'école d'ingénieur


# Installation

NB : Le projet utilise la version 3.12 de python.

## Cloner le dépôt Git

```sh
git clone https://github.com/LeRatdemare/Proxilearn.git
cd Proxilearn

## Créer l'environnement virtuel

python -m venv venv
venv\Scripts\activate    

## Installation des requirements

pip install -r requirements.txt

## Préparer la base de données

1. Appliquer les migrations
python manage.py migrate

2. Créer un super utilisateur pour accéder au Django admin 
python manage.py createsuperuser

# Tests

## Lancer l'environnement virtuel
python langage.py makemigrations
venv\Scripts\activate  

## Appliquer les migrations
python manage.py migrate

## Exécuter l'application
python manage.py runserver

## Utiliser le Django admin

Projet réalisé par Nathan Lufuluabo & Mathilde Dalphrase