#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Génération de Données de Ventes - Contexte Sénégalais
================================================================

Ce script génère un dataset synthétique de 50 000+ transactions de ventes
en respectant les réalités du marché sénégalais (prix, produits, saisonnalité).

Auteur: Oumaro Titans DJIGUIMDE
Date: Février 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration du seed pour la reproductibilité
np.random.seed(42)
random.seed(42)

# ============================================================================
# CONFIGURATION DES DONNÉES BASÉES SUR LE CONTEXTE SÉNÉGALAIS
# ============================================================================

# Villes principales du Sénégal avec leur poids commercial
VILLES = {
    'Dakar': 0.45,          # Capitale, ~45% des ventes
    'Thiès': 0.20,          # 2ème ville
    'Kaolack': 0.15,        # Hub commercial
    'Saint-Louis': 0.10,    # Ville historique
    'Ziguinchor': 0.10      # Sud, Casamance
}

# Catégories de produits et produits typiques du Sénégal
PRODUITS_PAR_CATEGORIE = {
    'Alimentation': {
        'Riz brisé 50kg': {'prix_base': 26000, 'variation': 0.10},
        'Riz parfumé 50kg': {'prix_base': 32000, 'variation': 0.12},
        'Huile palme 20L': {'prix_base': 17500, 'variation': 0.08},
        'Huile végétale 5L': {'prix_base': 5500, 'variation': 0.08},
        'Sucre cristallisé 50kg': {'prix_base': 30000, 'variation': 0.05},
        'Farine blé 50kg': {'prix_base': 28000, 'variation': 0.07},
        'Lait en poudre 1kg': {'prix_base': 4500, 'variation': 0.10},
        'Dattes 1kg': {'prix_base': 3000, 'variation': 0.15},
        'Café Touba 500g': {'prix_base': 2500, 'variation': 0.08},
        'Thé Lipton 200g': {'prix_base': 1800, 'variation': 0.05},
    },
    'Électronique': {
        'Samsung Galaxy A25': {'prix_base': 122000, 'variation': 0.05},
        'Infinix Note 50 Pro': {'prix_base': 149000, 'variation': 0.08},
        'Tecno Spark 40 5G': {'prix_base': 95000, 'variation': 0.10},
        'Huawei Nova 13': {'prix_base': 175000, 'variation': 0.05},
        'iPhone 12': {'prix_base': 450000, 'variation': 0.03},
        'Téléviseur LED 32"': {'prix_base': 125000, 'variation': 0.08},
        'Écouteurs Bluetooth': {'prix_base': 15000, 'variation': 0.12},
        'Chargeur rapide': {'prix_base': 8000, 'variation': 0.15},
        'Clé USB 32GB': {'prix_base': 5000, 'variation': 0.10},
        'Powerbank 10000mAh': {'prix_base': 12000, 'variation': 0.10},
    },
    'Textile': {
        'Tissu Wax 6 yards': {'prix_base': 18000, 'variation': 0.12},
        'Bazin riche 5 yards': {'prix_base': 35000, 'variation': 0.10},
        'Tissu Bogolan 3 yards': {'prix_base': 12000, 'variation': 0.15},
        'Dentelle Guipure 5 yards': {'prix_base': 25000, 'variation': 0.12},
        'Pagne Kenté 6 yards': {'prix_base': 22000, 'variation': 0.10},
        'Boubou brodé homme': {'prix_base': 45000, 'variation': 0.15},
        'Mboubou femme': {'prix_base': 38000, 'variation': 0.15},
        'Moussor femme': {'prix_base': 15000, 'variation': 0.12},
        'Sarouel coton': {'prix_base': 12000, 'variation': 0.10},
        'Voile hijab': {'prix_base': 3500, 'variation': 0.15},
    },
    'Électroménager': {
        'Réfrigérateur 180L': {'prix_base': 285000, 'variation': 0.08},
        'Climatiseur 12000 BTU': {'prix_base': 320000, 'variation': 0.10},
        'Ventilateur sur pied': {'prix_base': 35000, 'variation': 0.10},
        'Micro-ondes 20L': {'prix_base': 65000, 'variation': 0.08},
        'Cuisinière 4 feux': {'prix_base': 175000, 'variation': 0.10},
        'Fer à repasser': {'prix_base': 18000, 'variation': 0.12},
        'Bouilloire électrique': {'prix_base': 12000, 'variation': 0.10},
        'Mixeur': {'prix_base': 25000, 'variation': 0.10},
        'Machine à laver 7kg': {'prix_base': 195000, 'variation': 0.08},
        'Congélateur 200L': {'prix_base': 245000, 'variation': 0.08},
    },
    'Cosmétiques': {
        'Crème éclaircissante 500ml': {'prix_base': 8500, 'variation': 0.15},
        'Huile de coco 250ml': {'prix_base': 3500, 'variation': 0.12},
        'Parfum femme 100ml': {'prix_base': 25000, 'variation': 0.20},
        'Parfum homme 100ml': {'prix_base': 28000, 'variation': 0.20},
        'Henné naturel 100g': {'prix_base': 2500, 'variation': 0.10},
        'Savon noir Dudu Osun': {'prix_base': 1500, 'variation': 0.15},
        'Beurre de karité 500g': {'prix_base': 5000, 'variation': 0.12},
        'Huile d\'argan 100ml': {'prix_base': 12000, 'variation': 0.15},
        'Gel coiffant 500ml': {'prix_base': 4500, 'variation': 0.10},
        'Maquillage palette': {'prix_base': 18000, 'variation': 0.15},
    },
    'Construction': {
        'Ciment 50kg': {'prix_base': 4500, 'variation': 0.08},
        'Fer à béton 12mm': {'prix_base': 550, 'variation': 0.10},
        'Peinture 25L': {'prix_base': 35000, 'variation': 0.10},
        'Carrelage m²': {'prix_base': 8500, 'variation': 0.12},
        'Sable 1m³': {'prix_base': 25000, 'variation': 0.15},
        'Gravier 1m³': {'prix_base': 28000, 'variation': 0.15},
        'Briques creuses (unité)': {'prix_base': 200, 'variation': 0.10},
        'Tôles ondulées (unité)': {'prix_base': 12000, 'variation': 0.08},
        'Porte métallique': {'prix_base': 75000, 'variation': 0.10},
        'Fenêtre aluminium': {'prix_base': 45000, 'variation': 0.10},
    }
}

# Modes de paiement populaires au Sénégal
MODES_PAIEMENT = {
    'Orange Money': 0.35,
    'Wave': 0.30,
    'Espèces': 0.20,
    'Free Money': 0.08,
    'Carte bancaire': 0.05,
    'Wizall': 0.02
}

# Périodes spéciales avec hausse des ventes (contexte sénégalais)
PERIODES_SPECIALES = {
    'Ramadan': {
        'debut': '2024-03-11',
        'fin': '2024-04-09',
        'boost': 1.8,
        'categories_favorisees': ['Alimentation', 'Textile']
    },
    'Korité': {
        'debut': '2024-04-10',
        'fin': '2024-04-15',
        'boost': 2.5,
        'categories_favorisees': ['Textile', 'Cosmétiques', 'Alimentation']
    },
    'Tabaski': {
        'debut': '2024-06-10',
        'fin': '2024-06-20',
        'boost': 3.0,
        'categories_favorisees': ['Alimentation', 'Textile', 'Électroménager']
    },
    'Rentrée scolaire': {
        'debut': '2024-10-01',
        'fin': '2024-10-15',
        'boost': 2.0,
        'categories_favorisees': ['Textile', 'Électronique']
    },
    'Gamou': {
        'debut': '2024-09-15',
        'fin': '2024-09-20',
        'boost': 1.6,
        'categories_favorisees': ['Textile', 'Alimentation']
    },
    'Magal Touba': {
        'debut': '2024-08-20',
        'fin': '2024-08-25',
        'boost': 1.7,
        'categories_favorisees': ['Textile', 'Alimentation']
    },
    'Fin année': {
        'debut': '2024-12-15',
        'fin': '2024-12-31',
        'boost': 2.2,
        'categories_favorisees': ['Électronique', 'Électroménager', 'Textile']
    }
}

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def get_boost_factor(date, categorie):
    """
    Calcule le facteur de boost des ventes en fonction de la date et catégorie
    """
    boost = 1.0
    for periode, params in PERIODES_SPECIALES.items():
        debut = pd.to_datetime(params['debut'])
        fin = pd.to_datetime(params['fin'])
        
        if debut <= date <= fin:
            if categorie in params['categories_favorisees']:
                boost = max(boost, params['boost'])
            else:
                boost = max(boost, 1.2)  # Légère hausse générale
    
    return boost

def generer_quantite_realiste(categorie, prix_unitaire):
    """
    Génère une quantité réaliste selon la catégorie et le prix
    """
    if categorie == 'Alimentation':
        if prix_unitaire > 15000:  # Sacs de riz, sucre, etc.
            return np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
        else:  # Petits articles
            return np.random.choice([1, 2, 3, 4, 5, 10], p=[0.3, 0.3, 0.2, 0.1, 0.05, 0.05])
    
    elif categorie == 'Électronique':
        return np.random.choice([1, 2], p=[0.9, 0.1])  # Rarement plus de 2
    
    elif categorie == 'Textile':
        return np.random.choice([1, 2, 3, 4, 5], p=[0.4, 0.3, 0.15, 0.1, 0.05])
    
    elif categorie == 'Électroménager':
        return np.random.choice([1, 2], p=[0.95, 0.05])
    
    elif categorie == 'Construction':
        if prix_unitaire < 1000:  # Briques, fer
            return np.random.randint(10, 500)
        else:
            return np.random.choice([1, 2, 3, 5, 10], p=[0.3, 0.3, 0.2, 0.1, 0.1])
    
    else:
        return np.random.choice([1, 2, 3], p=[0.6, 0.3, 0.1])

def introduire_anomalies(df, taux_anomalies=0.02):
    """
    Introduit des anomalies volontaires pour tester le nettoyage
    """
    n_total = len(df)
    n_anomalies = int(n_total * taux_anomalies)
    
    # Valeurs manquantes aléatoires
    idx_manquantes = np.random.choice(df.index, size=n_anomalies//4, replace=False)
    colonnes = ['prix', 'quantite', 'mode_paiement']
    for idx in idx_manquantes:
        col = np.random.choice(colonnes)
        df.loc[idx, col] = np.nan
    
    # Prix aberrants (trop bas ou trop élevés)
    idx_prix = np.random.choice(df.index, size=n_anomalies//4, replace=False)
    for idx in idx_prix:
        if np.random.random() > 0.5:
            df.loc[idx, 'prix'] = df.loc[idx, 'prix'] * 0.01  # Prix ridiculement bas
        else:
            df.loc[idx, 'prix'] = df.loc[idx, 'prix'] * 10  # Prix trop élevé
    
    # Quantités aberrantes
    idx_qty = np.random.choice(df.index, size=n_anomalies//4, replace=False)
    for idx in idx_qty:
        df.loc[idx, 'quantite'] = np.random.choice([0, -1, 9999])
    
    # Doublons exacts
    idx_doublons = np.random.choice(df.index, size=n_anomalies//4, replace=False)
    df = pd.concat([df, df.loc[idx_doublons]], ignore_index=True)
    
    return df

# ============================================================================
# GÉNÉRATION DU DATASET
# ============================================================================

def generer_donnees_ventes(n_lignes=50000):
    """
    Génère le dataset complet de ventes
    """
    print(f"🔄 Génération de {n_lignes:,} lignes de données...")
    
    # Période de données : 1 an (2024)
    date_debut = datetime(2024, 1, 1)
    date_fin = datetime(2024, 12, 31)
    
    donnees = []
    
    for i in range(n_lignes):
        # Progression
        if (i + 1) % 5000 == 0:
            print(f"   ✓ {i+1:,} / {n_lignes:,} lignes générées")
        
        # Génération de la date (avec plus de ventes en fin de semaine)
        jours_totaux = (date_fin - date_debut).days
        jour = np.random.randint(0, jours_totaux)
        date = date_debut + timedelta(days=jour)
        
        # Week-end boost
        if date.weekday() >= 5:  # Samedi/Dimanche
            if np.random.random() > 0.3:
                pass
            else:
                continue
        
        # Sélection de la ville (distribution pondérée)
        ville = np.random.choice(list(VILLES.keys()), p=list(VILLES.values()))
        
        # Sélection de la catégorie et du produit
        categorie = np.random.choice(list(PRODUITS_PAR_CATEGORIE.keys()))
        produit = np.random.choice(list(PRODUITS_PAR_CATEGORIE[categorie].keys()))
        
        # Prix avec variation et boost saisonnier
        info_produit = PRODUITS_PAR_CATEGORIE[categorie][produit]
        prix_base = info_produit['prix_base']
        variation = info_produit['variation']
        
        # Application variation normale
        prix = prix_base * (1 + np.random.uniform(-variation, variation))
        
        # Application du boost saisonnier
        boost = get_boost_factor(pd.to_datetime(date), categorie)
        if boost > 1:
            # Pendant les fêtes, augmentation de la demande mais parfois promotion
            if np.random.random() > 0.3:
                prix = prix * np.random.uniform(0.95, 1.05)  # Légère variation
        
        # Quantité réaliste
        quantite = generer_quantite_realiste(categorie, prix)
        
        # Mode de paiement
        mode_paiement = np.random.choice(
            list(MODES_PAIEMENT.keys()), 
            p=list(MODES_PAIEMENT.values())
        )
        
        # Vendeur (ID fictif)
        vendeur = f"V{np.random.randint(1, 51):03d}"
        
        donnees.append({
            'date': date.strftime('%Y-%m-%d'),
            'produit': produit,
            'categorie': categorie,
            'prix': round(prix, 0),
            'quantite': quantite,
            'ville': ville,
            'mode_paiement': mode_paiement,
            'vendeur': vendeur
        })
    
    print(f"✅ Génération terminée : {len(donnees):,} transactions")
    
    # Création du DataFrame
    df = pd.DataFrame(donnees)
    
    # Calcul du chiffre d'affaires
    df['chiffre_affaires'] = df['prix'] * df['quantite']
    
    # Introduction d'anomalies pour le nettoyage
    print("🔧 Introduction d'anomalies volontaires (2%)...")
    df = introduire_anomalies(df, taux_anomalies=0.02)
    
    # Mélange final
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    return df

# ============================================================================
# STATISTIQUES DU DATASET
# ============================================================================

def afficher_statistiques(df):
    """
    Affiche des statistiques descriptives du dataset
    """
    print("\n" + "="*70)
    print("📊 STATISTIQUES DU DATASET GÉNÉRÉ")
    print("="*70)
    
    print(f"\n📌 Taille du dataset : {len(df):,} transactions")
    print(f"📅 Période : {df['date'].min()} → {df['date'].max()}")
    
    print(f"\n💰 Chiffre d'affaires total : {df['chiffre_affaires'].sum():,.0f} FCFA")
    print(f"💵 CA moyen par transaction : {df['chiffre_affaires'].mean():,.0f} FCFA")
    
    print("\n🏙️  Répartition par ville :")
    print(df['ville'].value_counts().to_string())
    
    print("\n📦 Répartition par catégorie :")
    print(df['categorie'].value_counts().to_string())
    
    print("\n💳 Répartition par mode de paiement :")
    print(df['mode_paiement'].value_counts().to_string())
    
    print("\n⚠️  Données manquantes :")
    print(df.isnull().sum().to_string())
    
    print("\n" + "="*70)

# ============================================================================
# EXÉCUTION PRINCIPALE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🇸🇳  GÉNÉRATEUR DE DONNÉES - VENTES SÉNÉGAL 🇸🇳")
    print("="*70)
    
    # Génération
    df = generer_donnees_ventes(n_lignes=50000)
    
    # Statistiques
    afficher_statistiques(df)
    
    # Sauvegarde
    output_path = 'data/sales_data.csv'
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n✅ Dataset sauvegardé : {output_path}")
    print(f"📊 Taille du fichier : {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    print("\n" + "="*70 + "\n")
