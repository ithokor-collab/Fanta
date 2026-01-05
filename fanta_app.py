import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(page_title="Fanta-Algoritmo 2026", page_icon="⚽")

# 1. FUNZIONE PER SCARICARE I DATI REALI (Senza Theo/Retegui fissi)
@st.cache_data(ttl=600) # Controlla aggiornamenti ogni 10 minuti
def scarica_dati_live():
    # URL di un database pubblico affidabile per la stagione 2025/2026
    url = "https://raw.githubusercontent.com/riccardomoriggi/fantalivescore/master/data/stats_aggiornate.csv"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            # Rimuoviamo eventuali rimasugli di vecchi dati se il server è lento
            df = df[df['Squadra'] != 'Esempio'] 
            return df
    except:
        return None

st.title("⚽ Radar Serie A 2025/2026")
st.write("Dati aggiornati in tempo reale dal database centrale.")

df = scarica_dati_live()

if df is not None:
    st.success(f"✅ Connesso! Analizzando {len(df)} calciatori attivi.")
    
    # Barra di ricerca per essere sicuri
    ricerca = st.text_input("Cerca un giocatore (es. Pulisic, Lautaro...):")
    if ricerca:
        risultati = df[df['Giocatore'].str.contains(ricerca, case=False, na=False)]
        st.table(risultati[['Giocatore', 'Squadra', 'Ruolo', 'MediaVoto']])
    
    st.subheader("Top 20 Giocatori del momento")
    st.dataframe(df.head(20))
else:
    st.error("⚠️ Il database esterno non risponde. Riprova tra pochi istanti.")
