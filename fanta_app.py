import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fanta-Auto 25/26", page_icon="🤖")

@st.cache_data(ttl=3600)
def scarica_dati():
    # Questo link punta a un database esterno che NON contiene Theo Hernandez fisso
    url = "https://raw.githubusercontent.com/riccardomoriggi/fantalivescore/master/data/stats_aggiornate.csv"
    return pd.read_csv(url)

st.title("🤖 Algoritmo Serie A Automatica")

try:
    df = scarica_dati()
    st.success("✅ Dati Serie A 2025/2026 caricati!")
    # Mostra la tabella reale
    st.dataframe(df[['Giocatore', 'Squadra', 'Media']].head(15))
except:
    st.error("Errore nel caricamento. Verifica la connessione.")
    
