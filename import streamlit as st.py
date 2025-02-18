import streamlit as st
import pandas as pd
from utils.data_processing import load_data

# Titre de l'application
st.title("Diamond Classification")

# Chargement des données
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Charger et traiter les données
    df = load_data(uploaded_file)

    # Afficher les données
    st.subheader("Processed Data")
    st.dataframe(df)

    # Graphiques ou analyses supplémentaires
    st.subheader("Color Distribution")
    st.bar_chart(df['Color'].value_counts())
