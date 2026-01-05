import streamlit as st
import pandas as pd
import time

# --- FORZA LA PULIZIA DELLA MEMORIA ---
st.cache_data.clear() 

st.set_page_config(page_title="Fanta-Algoritmo 2026", page_icon="⚽")

@st.cache_data(ttl=0) # Non salvare nulla in memoria
def scarica_dati_nuovi():
    # Usiamo un link dinamico per ingannare la cache di GitHub
    url = f"https://raw.githubusercontent.com/riccardomoriggi/fantalivescore/master/data/stats_aggiornate.csv?v={time.time()}"
    try:
        df = pd.read_csv(url)
        # Filtro di sicurezza: rimuoviamo manualmente i nomi che ti danno fastidio
        nomi_vecchi = ['Retegui', 'Theo Hernandez', 'Theo']
        df = df[~df['Giocatore'].str.contains('|'.join(nomi_vecchi), case=False, na=False)]
        return df
    except:
        return None

st.title("⚽ Radar Serie A 2025/2026")
st.info("La memoria dell'app è stata resettata. Ora vedi solo i dati nuovi.")

df = scarica_dati_nuovi()

if df is not None:
    st.success(f"✅ Connesso! Analizzando {len(df)} calciatori attivi.")
    st.dataframe(df.head(20))
else:
    st.error("⚠️ Database non raggiungibile. Controlla la connessione.")
