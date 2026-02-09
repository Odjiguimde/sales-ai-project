# 🇸🇳 Projet d'Ingénierie de Données et Analyse des Ventes (Contexte Sénégalais)

## 📌 Présentation du projet

Ce projet illustre un workflow complet d'ingénierie de données et d'analyse à l'aide de Python et SQL, appliqué à un jeu de données de ventes de grande taille, **inspiré du contexte commercial sénégalais**.

L'objectif est de reproduire des situations réelles rencontrées en entreprise : génération de données, ingestion, nettoyage, transformation et analyse analytique, telles qu'attendues d'un ingénieur data / ingénieur IA junior.

---

## 🎯 Objectifs du projet

✅ Concevoir et manipuler un jeu de données structuré de grande taille (45 000+ lignes)  
✅ Appliquer les bonnes pratiques de l'ingénierie de données  
✅ Réaliser des analyses SQL avancées orientées business  
✅ Construire un pipeline de données clair et reproductible  
✅ Démontrer une forte capacité de raisonnement sur la donnée  

---

## 🗂 Description du jeu de données

### 📄 Type de données
- Jeu de données **simulé** 
- Inspiré de **schémas commerciaux réalistes au Sénégal**
- Basé sur des recherches approfondies du marché sénégalais (prix officiels, produits typiques, saisonnalité)

### 📦 Taille
- Environ **45 965 enregistrements**
- Période : **Année 2024 complète**
- CA total : **3,49 milliards FCFA**

### 📑 Colonnes

| Colonne | Description |
|---------|-------------|
| `date` | Date de la transaction |
| `produit` | Nom du produit |
| `categorie` | Catégorie du produit |
| `prix` | Prix unitaire (FCFA) |
| `quantite` | Quantité vendue |
| `ville` | Ville de vente |
| `mode_paiement` | Mode de paiement utilisé |
| `vendeur` | Identifiant du vendeur |
| `chiffre_affaires` | CA de la transaction |

### 🌍 Villes concernées
- **Dakar** (45% des ventes) - Capitale économique
- **Thiès** (20%) - 2ème ville du pays
- **Kaolack** (15%) - Hub commercial central
- **Saint-Louis** (10%) - Ville historique du nord
- **Ziguinchor** (10%) - Casamance, sud du pays

### 📦 Catégories de produits

Le dataset reflète le commerce sénégalais avec **6 catégories** :

1. **Alimentation** : Riz (brisé, parfumé), Huile (palme, végétale), Sucre, Dattes, Café Touba, etc.
2. **Électronique** : Smartphones (Samsung, Infinix, Tecno, Huawei, iPhone), Accessoires
3. **Textile** : Tissu Wax, Bazin, Bogolan, Dentelle, Boubous traditionnels
4. **Électroménager** : Réfrigérateurs, Climatiseurs, Ventilateurs, Cuisinières
5. **Cosmétiques** : Crèmes, Huiles (coco, argan), Henné, Beurre de karité
6. **Construction** : Ciment, Fer à béton, Peinture, Carrelage

### 💳 Modes de paiement (réalité sénégalaise)

- **Orange Money** (35%) - Leader historique
- **Wave** (30%) - Challenger récent très populaire
- **Espèces** (20%) - Toujours présent
- **Free Money** (8%)
- **Carte bancaire** (5%) - Faible taux de bancarisation
- **Wizall** (2%)

### 🎉 Saisonnalité (fêtes et périodes commerciales)

Le dataset intègre les **pics de ventes** liés aux événements sénégalais :

- **Ramadan** (mars) → +80% ventes Alimentation & Textile
- **Korité** (avril) → +150% (fin du Ramadan)
- **Tabaski** (juin) → +200% (fête du mouton - pic commercial annuel)
- **Magal de Touba** (août) → +70%
- **Gamou** (septembre) → +60%
- **Rentrée scolaire** (octobre) → +100%
- **Fin d'année** (décembre) → +120%

### 📌 Remarque sur la qualité des données

Les données ont été volontairement enrichies avec :
- ✅ **Prix réalistes** issus de sources officielles (Ministère du Commerce, PrixDakar.com)
- ✅ **Anomalies intentionnelles** (2%) pour tester les compétences de nettoyage :
  - Valeurs manquantes
  - Prix aberrants
  - Quantités négatives ou nulles
  - Doublons exacts

---

## 🛠 Technologies utilisées

- **Python 3.12**
- **Pandas** - Manipulation de données
- **NumPy** - Calculs numériques
- **SQL** (compatible SQLite / PostgreSQL)
- **Jupyter Notebook** - Analyses interactives
- **Git & GitHub** - Versioning

---

## 🏗 Structure du projet

```
sales-data-engineering/
│
├── data/
│   └── sales_data.csv           # Dataset généré (45 965 lignes)
│
├── notebooks/
│   ├── 01_exploration_donnees.ipynb    # Exploration initiale
│   ├── 02_nettoyage_donnees.ipynb      # Data cleaning
│   └── 03_analyse_sql.ipynb            # Requêtes SQL avancées
│
├── scripts/
│   └── generation_donnees.py           # Script de génération
│
├── README.md                    # Documentation (ce fichier)
└── requirements.txt             # Dépendances Python
```

---

## 🔄 Pipeline de traitement des données

### 1️⃣ Génération des données
- Création d'un dataset synthétique avec Python
- Application de règles métiers (prix FCFA, quantités, villes, saisonnalité)
- Respect du contexte commercial sénégalais

### 2️⃣ Ingestion
- Chargement du fichier CSV avec Pandas
- Vérification du schéma des données

### 3️⃣ Nettoyage
- Détection et traitement des valeurs manquantes
- Normalisation des types
- Vérification des valeurs aberrantes
- Suppression des doublons

### 4️⃣ Transformation
- Calcul du chiffre d'affaires
- Agrégations par ville, catégorie et période
- Enrichissement avec indicateurs métiers

### 5️⃣ Analyses SQL
- Requêtes `JOIN`, `GROUP BY`, `HAVING`
- Fonctions analytiques (`WINDOW FUNCTIONS`)
- Extraction d'indicateurs clés (KPI)

---

## 📈 Principaux indicateurs analysés

- 🏆 Produits générant le plus de chiffre d'affaires
- 🌍 Performance des ventes par ville
- 📅 Évolution mensuelle du chiffre d'affaires
- 📊 Contribution des catégories au CA total
- 💎 Identification des ventes à forte valeur
- 💳 Répartition par mode de paiement
- 📈 Impact de la saisonnalité (Tabaski, Ramadan, etc.)

---

## 💡 Intérêt du projet

✔️ Reflète un travail **réel d'ingénierie de données**  
✔️ Montre une capacité à traiter de **grands volumes de données**  
✔️ Met en valeur une **bonne maîtrise du SQL**  
✔️ Adapté au **contexte africain et sénégalais**  
✔️ Pertinent pour les **stages et premiers emplois**  
✔️ Démontre une capacité de **recherche et contextualisation**  

---

## 🚀 Exécution du projet

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Génération des données

```bash
python scripts/generation_donnees.py
```

**Résultat attendu :**
```
✅ Dataset sauvegardé : data/sales_data.csv
📊 Taille du fichier : 20.63 MB
💰 Chiffre d'affaires total : 3,490,720,809 FCFA
```

### Exploration et analyse

Ouvrir les notebooks Jupyter dans l'ordre :
```bash
jupyter notebook notebooks/
```

---

## 🎓 Compétences démontrées

### Compétences techniques
- 🐍 **Python** : Pandas, NumPy, génération de données
- 🗄️ **SQL** : Requêtes avancées, agrégations, window functions
- 📊 **Analyse de données** : Statistiques descriptives, visualisation
- 🧹 **Data Cleaning** : Détection et traitement des anomalies
- 🔄 **ETL** : Pipeline complet Extract-Transform-Load

### Compétences méthodologiques
- 🔍 **Recherche documentaire** : Sources officielles (Ministère, sites sénégalais)
- 🎯 **Contextualisation** : Adaptation au marché local
- 📝 **Documentation** : Code commenté, README détaillé
- 🧪 **Qualité** : Introduction volontaire d'anomalies pour tests

---

## 🔮 Améliorations futures

- [ ] Intégration avec **PostgreSQL**
- [ ] Orchestration du pipeline avec **Apache Airflow**
- [ ] Validation des données (**Great Expectations**)
- [ ] Tableau de bord interactif (**Power BI / Tableau**)
- [ ] Modèle de prédiction du CA (**Machine Learning**)
- [ ] API REST pour exposer les données
- [ ] Tests unitaires avec **pytest**

---

## 👤 Auteur

**Oumaro Titans DJIGUIMDE**  
Étudiant en Ingénierie de Données et Intelligence Artificielle  
📍 Sénégal  

---

## 📊 Sources et Références

Ce projet s'appuie sur des **données réelles du marché sénégalais** :

### Prix officiels
- [Ministère des Finances - Baisse des prix 2024](https://www.finances.gouv.sn/baisse-des-prix-au-senegal-liste-des-mesures-prises-par-le-gouvernement/)
- [PrixDakar.com - Comparateur de prix](https://prixdakar.com/)
- Gouvernement du Sénégal - Arrêtés de prix

### Produits et marché
- Boutiques Orange, Electroménager Dakar, Nova.sn
- Marché Sandaga, Castors (Dakar)
- Commerce de tissus wax (SOTIBA, SIMPAFRIC)

### Modes de paiement
- PayTech, SenePay - Solutions de paiement mobile
- Orange Money, Wave - Statistiques d'utilisation

### Saisonnalité
- Calendrier des fêtes religieuses 2024-2025
- Commission nationale du croissant lunaire (CONACOC)
- Études sur l'économie de la Tabaski (Inter-Réseaux)

---

## 📣 Mot de fin

Ce projet a été conçu avec une **approche professionnelle**, en respectant les **standards de l'industrie**, afin de maximiser l'attractivité du profil pour les **entreprises tech** et démontrer une **maîtrise technique et contextuelle** de l'ingénierie de données.

Le choix d'un contexte sénégalais reflète une **volonté de valoriser les réalités locales** et de montrer une capacité à **adapter les compétences techniques au terrain**.

---

⭐ **Si ce projet vous intéresse, n'hésitez pas à le cloner et l'adapter à vos besoins !**
