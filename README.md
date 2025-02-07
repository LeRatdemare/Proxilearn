# 📚 Proxylearn - Apprentissage Adaptatif avec l'IA

Proxylearn est un projet d'intégration de l'intelligence artificielle pour la personnalisation des parcours d'apprentissage en fonction du niveau et des besoins des élèves. Il repose sur l'algorithme ZPDES (Zone Proximale de Développement et Exploration Séquentielle), inspiré des bandits multi-bras.
Il s'incrit dns le cadre d'un projet de parcours d'école d'ingénieur

# Installation

NB : Le projet utilise la version 3.12 de python.

## Cloner le dépôt Git

Ouvrir un terminal et saisir la commande `git clone https://github.com/LeRatdemare/Proxilearn.git` pour cloner le dépôt Git en local.

## Créer l'environnement virtuel

Pour créer un environnement virtuel, se placer dans le dossier racine où se trouve le fichier "README.md" puis saisir la commande `python3.12 -m venv env`.

Une fois l'environnement créé, il faudra l'activer en entrant la commande `source env/Scripts/activate` (ou `source env/bin/activate` sur Mac et Linux).

## Installation des requirements

La liste des dépendances du projet est contenue dans le fichier "requirements.txt". Pour mettre à jour le projet local, vérifier que l'environnement virtuel soit activé puis entrer la commande `pip install -r requirements.txt`.

## Préparer la base de données

1. Appliquer les migrations : `python manage.py migrate`
2. Créer un super utilisateur pour accéder au Django admin `python manage.py createsuperuser`

# Tests

## Lancer l'environnement virtuel

Depuis le dossier racine du projet, entrer `source env/Scripts/activate` (ou `source env/bin/activate` sur Mac et Linux) dans un terminal.

## Appliquer les migrations

S'assurer que la base de donnée est bien mise à jour en saisissant : `python manage.py migrate`.

S'il y a un problème, ne pas hésiter à supprimer manuellement la base de donnée (fichier "proxilearn/db.sqlite3") avant de recommencer la manipulation.

## Exécuter l'application

Depuis le dossier "proxilearn" ou un de ses sous-dossiers, exécuter `python manage.py runserver` dans un terminal.

## Utiliser le Django admin

Pour manipuler manuellement la base de donnée (créer/modifier/supprimer des lignes), il faut avoir créé un compte superuser. Suite à ça, lancer l'application et se connecter au [Django admin](http://127.0.0.1:8000/admin) en ajoutant "/admin" après le nom de domaine (probablement http://127.0.0.1:8000 si lancement en local).

# Crédits

Projet réalisé par Nathan Lufuluabo & Mathilde Dalphrase