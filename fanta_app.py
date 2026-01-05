import streamlit as st
import pandas as pd
import numpy as np
from pulp import *

# Impostazioni interfaccia per cellulare
st.set_page_config(page_title="Fanta-Assistant 2026", page_icon="⚽")

st.title("⚽ Il Mio Fanta-Algoritmo")
st.write("Formazione ottimizzata basata su Media Voto, Forma e xG.")

# 1. DATABASE GIOCATORI (Esempio aggiornato)
@st.cache_data(ttl=3600)
def carica_dati():
    data = {
        'Giocatore': ['Sommer', 'Maignan', 'Di Lorenzo', 'Theo', 'Dimarco', 'Comuzzo', 'Pulisic', 'Zaccagni', 'Barella', 'Nico Paz', 'Lautaro', 'Lookman', 'Retegui', 'Vlahovic'],
        'Ruolo': ['P', 'P', 'D', 'D', 'D', 'D', 'C', 'C', 'C', 'C', 'A', 'A', 'A', 'A'],
        'MediaVoto': [6.2, 6.1, 6.4, 6.5, 6.6, 6.1, 7.1, 6.8, 6.5, 6.7, 7.5, 7.3, 7.2, 7.0],
        'xG_xA': [0.1, 0.0, 0.3, 0.4, 0.5, 0.1, 0.9, 0.7, 0.4, 0.8, 1.2, 1.1, 1.0, 0.8], 
        'Forma': [70, 55, 80, 75, 85, 65, 95, 88, 75, 92, 98, 94, 90, 40],
        'Titolarita': [100, 100, 100, 100, 95, 85, 100, 100, 95, 90, 100, 100, 100, 0]
    }
    return pd.DataFrame(data)

df = carica_dati()

# 2. CALCOLO DELLO SCORE (L'algoritmo decisionale)
df['Score'] = (df['MediaVoto'] * 2) + (df['xG_xA'] * 5) + (df['Forma'] / 10)

# 3. OTTIMIZZATORE MATEMATICO (Modulo 3-4-3)
prob = LpProblem("Fanta", LpMaximize)
gioc = LpVariable.dicts("G", df.index, cat='Binary')

# Obiettivo: massimizzare lo Score totale della squadra
prob += lpSum([df.loc[i, 'Score'] * gioc[i] for i in df.index])

# Vincoli tattici (11 totali, 1 portiere, 3 difensori, 4 centrocampisti, 3 attaccanti)
prob += lpSum([gioc[i] for i in df.index]) == 11
prob += lpSum([gioc[i] for i in df.index if df.loc[i, 'Ruolo'] == 'P']) == 1
prob += lpSum([gioc[i] for i in df.index if df.loc[i, 'Ruolo'] == 'D']) == 3
prob += lpSum([gioc[i] for i in df.index if df.loc[i, 'Ruolo'] == 'C']) == 4
prob += lpSum([gioc[i] for i in df.index if df.loc[i, 'Ruolo'] == 'A']) == 3

prob.solve(PULP_CBC_CMD(msg=0))

# 4. VISUALIZZAZIONE RISULTATI
st.subheader("🚀 La Top 11 Consigliata")

for i in df.index:
    if gioc[i].varValue == 1:
        with st.expander(f"{df.loc[i, 'Ruolo']} - {df.loc[i, 'Giocatore']}"):
            st.write(f"📈 Score Algoritmo: **{df.loc[i, 'Score']:.1f}**")
            st.write(f"🎯 Pericolosità (xG): {df.loc[i, 'xG_xA']}")
            st.progress(int(df.loc[i, 'Forma']) / 100)
            st.caption(f"Stato di forma: {df.loc[i, 'Forma']}%")

st.divider()
if st.button('🔄 Ricalcola Formazione'):
    st.rerun()
  
