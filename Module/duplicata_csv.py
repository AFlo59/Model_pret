import os
import pandas as pd

def verifier_doublons(df):
    # Créer une colonne temporaire pour identifier les doublons
    df['doublons'] = df.duplicated(keep=False)
    
    # Créer un dictionnaire pour stocker les doublons de chaque échantillon
    doublons_par_echantillon = {}
    
    # Itérer à travers les lignes du DataFrame
    for index, row in df.iterrows():
        # Identifier l'index de l'échantillon
        index_echantillon = (row.drop('doublons')).to_string()
        
        # Vérifier si l'échantillon est un doublon
        if row['doublons']:
            # Ajouter l'échantillon à la liste des doublons
            if index_echantillon not in doublons_par_echantillon:
                doublons_par_echantillon[index_echantillon] = []
            doublons_par_echantillon[index_echantillon].append(index)
    
    # Supprimer les doublons du DataFrame
    df.drop_duplicates(inplace=True)
    
    # Supprimer la colonne temporaire des doublons
    df.drop(columns=['doublons'], inplace=True)
    
    return doublons_par_echantillon, df
