import os
import sys
import streamlit as st 
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler, OneHotEncoder, PolynomialFeatures
from datetime import datetime, timedelta
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Lasso

sys.path.append('../Module')
folder_path = '../Model'

from pickle_job import charger_modele
loaded_model = charger_modele(folder_path + '/catboost_model.pkl')

# Titre de l'application
st.title('Prédiction de prêt')
model = loaded_model

st.header('Entrez les données du prêt')
name = st.text_input('Nom de l\'entreprise')
city = st.text_input('Ville')
state = st.selectbox('État', ['AL', 'AK', 'AZ', 'AR', 'CA'])  # Remplacez par les états pertinents
bank = st.text_input('Banque')
bank_state = st.selectbox('État de la banque', ['AL', 'AK', 'AZ', 'AR', 'CA'])  # Remplacez par les états pertinents
naics = st.text_input('NAICS')
approval_date = st.date_input('Date d\'approbation')
approval_fy = st.number_input('Année d\'approbation', min_value=1970, max_value=2030)
term = st.number_input('Durée du prêt (en mois)')
no_emp = st.number_input('Nombre d\'employés')
new_exist = st.selectbox('Nouvelle ou Existante', [1, 2])
create_job = st.number_input('Emplois créés')
retained_job = st.number_input('Emplois maintenus')
urban_rural = st.selectbox('Rural ou Urbain', ['Rural', 'Urban'])
rev_line_cr = st.selectbox('Ligne de crédit renouvelable', [True, False])
low_doc = st.selectbox('Faible documentation', [True, False])
gr_appv = st.number_input('Montant approuvé par le gouvernement')
sba_appv = st.number_input('Montant approuvé par la SBA')
franchise = st.selectbox('Franchise', [1, 0])

# Préparer les données pour la prédiction
data = pd.DataFrame({
    'Name': [name],
    'City': [city],
    'State': [state],
    'Bank': [bank],
    'BankState': [bank_state],
    'NAICS': [naics],
    'ApprovalDate': [approval_date],
    'ApprovalFY': [approval_fy],
    'Term': [term],
    'NoEmp': [no_emp],
    'NewExist': [new_exist],
    'CreateJob': [create_job],
    'RetainedJob': [retained_job],
    'UrbanRural': [urban_rural],
    'RevLineCr': [rev_line_cr],
    'LowDoc': [low_doc],
    'GrAppv': [gr_appv],
    'SBA_Appv': [sba_appv],
    'Franchise': [franchise]
})

# Faire une prédiction lorsque l'utilisateur appuie sur le bouton
if st.button('Prédire'):
    prediction = model.predict(data)
    if prediction[0] == 1:
        st.success('La demande de prêt est approuvée !')
    else:
        st.error('La demande de prêt est refusée.')