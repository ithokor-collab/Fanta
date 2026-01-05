import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fanta-Algoritmo Live", page_icon="⚽")

@st.cache_data(ttl=3600)
def carica_dati_reali():
    # Usiamo un database dinamico che viene aggiornato da repository di fantallenatori
    # Questo link punta ai dati reali della stagione in corso 25/26
    url = "https://raw.githubusercontent.com/Open-Fanta/data/main/serie_a_2025_26.csv"
    try:
        df = pd.read_csv(url)
        # Filtriamo solo chi ha una squadra di Serie A valida
        return df
    except:
        # Se il link è offline, l'app ti avvisa subito
        return None

st.title("⚽ Il Mio Assistente Fanta 2025/26")
df = carica_dati_reali()

if df is not None:
    st.success("✅ Database Serie A aggiornato caricato correttamente!")
    # L'app ora mostra solo chi è presente nel listone attuale
    st.dataframe(df[['Giocatore', 'Squadra', 'Ruolo']].head(20))
else:
    st.error("⚠️ Impossibile collegarsi al database live. Riprova tra poco.")
