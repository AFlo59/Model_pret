import os
import sys
import streamlit as st
import pandas as pd
import pickle

sys.path.append('../Module')
folder_path = '../Model'


from pickle_job import charger_modele

loaded_model = charger_modele(folder_path + '/catboost_model.pkl')

st.title('Prédiction de prêt')

# Charger le modèle
model = loaded_model

# Afficher un formulaire pour saisir les données d'entrée
st.header('Entrez les données du prêt')
city = st.text_input('Ville')
state = st.selectbox('État', ['AL', 'AK', 'AZ', 'AR', 'CA'])  # Remplacez par les états pertinents
term = st.number_input('Durée du prêt (en mois)')
no_emp = st.number_input('Nombre d\'employés')
# Ajoutez d'autres champs ici...

# Préparer les données pour la prédiction
data = pd.DataFrame({
    'City': [city],
    'State': [state],
    'Term': [term],
    'NoEmp': [no_emp]
    # Ajoutez d'autres colonnes ici...
})

# Faire une prédiction lorsque l'utilisateur appuie sur le bouton
if st.button('Prédire'):
    prediction = model.predict(data)
    if prediction[0] == 1:
        st.success('La demande de prêt est approuvée !')
    else:
        st.error('La demande de prêt est refusée.')