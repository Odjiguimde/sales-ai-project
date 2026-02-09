📊 Projet d’Ingénierie de Données et Analyse des Ventes (Contexte Sénégalais)
📌 Présentation du projet

Ce projet illustre un workflow complet d’ingénierie de données et d’analyse à l’aide de Python et SQL, appliqué à un jeu de données de ventes de grande taille, inspiré du contexte commercial sénégalais.

L’objectif est de reproduire des situations réelles rencontrées en entreprise : génération de données, ingestion, nettoyage, transformation et analyse analytique, telles qu’attendues d’un ingénieur data / ingénieur IA junior.

🎯 Objectifs du projet

Concevoir et manipuler un jeu de données structuré de grande taille (50 000+ lignes)

Appliquer les bonnes pratiques de l’ingénierie de données

Réaliser des analyses SQL avancées orientées business

Construire un pipeline de données clair et reproductible

Démontrer une forte capacité de raisonnement sur la donnée

🗂 Description du jeu de données
📄 Type de données

Jeu de données simulé

Inspiré de schémas commerciaux réalistes au Sénégal

📦 Taille

Environ 50 000 enregistrements

📑 Colonnes
Colonne	Description
date	Date de la transaction
produit	Nom du produit
categorie	Catégorie du produit
prix	Prix unitaire (FCFA)
quantite	Quantité vendue
ville	Ville de vente
🌍 Villes concernées

Dakar

Thiès

Saint-Louis

Kaolack

Ziguinchor

📌 Remarque : Les données ont été volontairement simulées afin de garantir la maîtrise de la qualité, une pratique courante en ingénierie de données.

🛠 Technologies utilisées

Python 3

Pandas

SQL (compatible SQLite / PostgreSQL)

Google Colab

Git & GitHub

🏗 Structure du projet
sales-data-engineering/
│
├── data/
│   └── sales_data.csv
│
├── notebooks/
│   ├── 01_exploration_donnees.ipynb
│   ├── 02_nettoyage_donnees.ipynb
│   └── 03_analyse_sql.ipynb
│
├── scripts/
│   └── generation_donnees.py
│
├── README.md
└── requirements.txt

🔄 Pipeline de traitement des données

Génération des données

Création d’un dataset synthétique avec Python

Application de règles métiers (prix, quantités, villes)

Ingestion

Chargement du fichier CSV avec Pandas

Vérification du schéma des données

Nettoyage

Détection et traitement des valeurs manquantes

Normalisation des types

Vérification des valeurs aberrantes

Transformation

Calcul du chiffre d’affaires

Agrégations par ville, catégorie et période

Analyses SQL

Requêtes JOIN, GROUP BY, HAVING

Fonctions analytiques (window functions)

Extraction d’indicateurs clés (KPI)

📈 Principaux indicateurs analysés

Produits générant le plus de chiffre d’affaires

Performance des ventes par ville

Évolution mensuelle du chiffre d’affaires

Contribution des catégories au chiffre d’affaires total

Identification des ventes à forte valeur

💡 Intérêt du projet

✔️ Reflète un travail réel d’ingénierie de données
✔️ Montre une capacité à traiter de grands volumes de données
✔️ Met en valeur une bonne maîtrise du SQL
✔️ Adapté au contexte africain et sénégalais
✔️ Pertinent pour les stages et premiers emplois

🚀 Améliorations futures

Intégration avec PostgreSQL

Orchestration du pipeline avec Airflow

Validation des données (Great Expectations)

Tableau de bord (Power BI / Tableau)

Modèle de prédiction du chiffre d’affaires (Machine Learning)

👤 Auteur

Oumaro Titans DJIGUIMDE
Étudiant en Ingénierie de Données et Intelligence Artificielle
📍 Sénégal

⭐ Exécution du projet
pip install -r requirements.txt

python scripts/generation_donnees.py

📣 Mot de fin

Ce projet a été conçu avec une approche professionnelle, en respectant les standards de l’industrie, afin de maximiser l’attractivité du profil pour les entreprises tech.
