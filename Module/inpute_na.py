import os
import pandas as pd

def traiter_valeurs_manquantes(df, seuil=0.5):
    # Calculer le pourcentage de valeurs manquantes pour chaque colonne
    pourcentage_valeurs_manquantes = df.isnull().mean()

    # Filtrer les colonnes avec un pourcentage de valeurs manquantes supérieur au seuil
    colonnes_a_supprimer = pourcentage_valeurs_manquantes[pourcentage_valeurs_manquantes > seuil].index
    df.drop(columns=colonnes_a_supprimer, inplace=True)

    # Séparer les colonnes numériques et catégorielles restantes
    colonnes_numeriques = df.select_dtypes(include=['number']).columns
    colonnes_categorielles = df.select_dtypes(include=['object']).columns

    # Remplir les valeurs manquantes pour les colonnes numériques avec la moyenne
    for colonne in colonnes_numeriques:
        if df[colonne].isnull().any():
            moyenne = df[colonne].mean()
            df[colonne].fillna(moyenne, inplace=True)

    # Remplir les valeurs manquantes pour les colonnes catégorielles avec la valeur la plus fréquente
    for colonne in colonnes_categorielles:
        if df[colonne].isnull().any():
            valeur_frequente = df[colonne].mode()[0]
            df[colonne].fillna(valeur_frequente, inplace=True)

    return df
