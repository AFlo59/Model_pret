def display_unique_categorical_values(df):
    """
    Affiche les valeurs uniques de chaque colonne catégorielle dans un DataFrame,
    ainsi que leur pourcentage et leur nombre brut.

    Args:
        df (pandas.DataFrame): Le DataFrame à analyser.
    """
    for column in df.select_dtypes(include=['object', 'category']).columns:
        total_count = df[column].count()
        unique_values = df[column].value_counts()
        print(f"Colonne '{column}':")
        for value, count in unique_values.items():
            percentage = (count / total_count) * 100
            print(f"- {value}: {count} ({percentage:.2f}%)")
        print("\n")