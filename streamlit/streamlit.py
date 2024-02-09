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
model = charger_modele(folder_path + '/catboost_model.pkl')

# Titre de l'application
st.title('Prédiction de prêt')


st.header('Entrez les données du prêt')

name = st.text_input('Nom de l\'entreprise')

city = st.text_input('Ville')

us_states = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY"
}
state_names = list(us_states.keys())


selected_state = st.selectbox('État', state_names)
state = us_states[selected_state]
st.write("Abréviation de l'État :", state)

bank = st.text_input('Nom de la Banque')

selected_bankstate = st.selectbox('État de la banque', state_names)
bank_state = us_states[selected_bankstate]
st.write("État de votre banque", bank_state)

naics_mapping = {
    "Agriculture, forestry, fishing and hunting": "11",
    "Mining, quarrying, and oil and gas extraction": "21",
    "Utilities": "22",
    "Construction": "23",
    "Manufacturing": "31-33",
    "Wholesale trade": "42",
    "Retail trade": "44-45",
    "Transportation and warehousing": "48-49",
    "Information": "51",
    "Finance and insurance": "52",
    "Real estate and rental and leasing": "53",
    "Professional, scientific, and technical services": "54",
    "Management of companies and enterprises": "55",
    "Administrative and support and waste management and remediation services": "56",
    "Educational services": "61",
    "Health care and social assistance": "62",
    "Arts, entertainment, and recreation": "71",
    "Accommodation and food services": "72",
    "Other services (except public administration)": "81",
    "Public administration": "92"
}
selected_description = st.selectbox("Sélectionnez une description NAICS", list(naics_mapping.keys()))

naics = naics_mapping[selected_description]
st.write("Numéro NAICS :", naics)

def convert_date_format(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%d/%b/%y")
        formatted_date = date_obj.strftime("%d-%m-%y")
        return formatted_date
    except ValueError:
        return ""
    
approval_date_str = st.text_input('Date d\'approbation (ex: 29/jan/96)')
approval_date = convert_date_format(approval_date_str)
st.write(f"Date : {approval_date}")

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