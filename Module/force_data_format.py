import os
import pandas as pd

def force_data_format(df):
    """
    Force la mise en forme de chaque colonne du DataFrame en utilisant le type de valeur le plus fréquent dans chaque colonne.
    
    Args:
        df (pandas.DataFrame): Le DataFrame à formater.
    
    Returns:
        pandas.DataFrame: Le DataFrame avec la mise en forme forcée.
    """
    def get_columns_with_invalid_values(df):
        """
        Récupère les noms des colonnes contenant des valeurs non valides dans un DataFrame.
        
        Args:
            df (pandas.DataFrame): Le DataFrame à vérifier.
        
        Returns:
            list: Une liste contenant les noms des colonnes avec des valeurs non valides.
        """
        invalid_columns = []
        for column in df.columns:
            try:
                pd.to_numeric(df[column], errors='raise', downcast='integer')
            except ValueError:
                invalid_columns.append(column)
        return invalid_columns
    
    for column in df.columns:
        most_common_type = df[column].apply(type).mode().iloc[0]
        if most_common_type == int:
            # Si le type le plus fréquent est un entier, convertissez les valeurs à NaN si elles ne peuvent pas être converties en entier
            df[column] = pd.to_numeric(df[column], errors='coerce', downcast='integer')
        elif most_common_type == float:
            # Si le type le plus fréquent est un flottant, convertissez les valeurs à NaN si elles ne peuvent pas être converties en flottant
            df[column] = pd.to_numeric(df[column], errors='coerce', downcast='float')
        else:
            # Si le type le plus fréquent est une chaîne de caractères, conservez-le tel quel
            df[column] = df[column].astype(str)
    
    invalid_columns = get_columns_with_invalid_values(df)
    print("Colonnes avec des valeurs non valides :", invalid_columns)
    
    return df
