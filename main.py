import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Preditor Pro 2026", layout="wide")
st.title("🎯 Analisador de Tendências: Próximos Jogos")

api_key = 'c9f55dc0e91ac61caf1e05371daa9a8c'
headers = {'x-rapidapi-key': api_key}

# IDs Principais Brasileirão
times_ids = {
    "Flamengo": 127, "Palmeiras": 121, "Botafogo": 120, "Bahia": 118, 
    "São Paulo": 126, "Corinthians": 117, "Cruzeiro": 131, "Fortaleza": 154
}

st.sidebar.header("Análise de Confronto")
time_casa = st.sidebar.selectbox("Time da Casa", list(times_ids.keys()))
time_fora = st.sidebar.selectbox("Time Visitante", list(times_ids.keys()))

def pegar_tendencia(team_id):
    # Buscamos as estatísticas GERAIS da liga para o time
    url = f"https://v3.football.api-sports.io/teams/statistics?league=71&season=2025&team={team_id}"
    res = requests.get(url, headers=headers).json().get('response', {})
    
    # Se a API Free negar a média, nós calculamos manualmente ou usamos padrão seguro
    stats = {
        "cantos_med": res.get('corners', {}).get('avg', {}).get('total', 0) or 5.2, # Média base se falhar
        "cartoes_med": res.get('cards', {}).get('yellow', {}).get('total', 0) or 2.1,
        "gols_feitos": float(res.get('goals', {}).get('for', {}).get('average', {}).get('total', 0) or 0),
        "gols_sofridos": float(res.get('goals', {}).get('against', {}).get('average', {}).get('total', 0) or 0)
    }
    return stats

if st.button('🎲 Calcular Probabilidades do Jogo'):
    with st.spinner('Cruzando dados históricos...'):
        casa = pegar_tendencia(times_ids[time_casa])
        fora = pegar_tendencia(times_ids[time_fora])
        
        # LÓGICA DE PREVISÃO (Cálculo de Tendência)
        pred_cantos = casa['cantos_med'] + fora['cantos_med']
        pred_amarelos = casa['cartoes_med'] + fora['cartoes_med']
        
        # Probabilidade de Ambas Marcam
        prob_btts = (casa['gols_feitos'] + fora['gols_sofridos']) / 2
        status_btts = "🔥 ALTA" if prob_btts > 1.2 else "⚠️ MODERADA"

        # Exibição Visual
        c1, c2, c3 = st.columns(3)
        c1.metric("Projeção de Escanteios", f"{pred_cantos:.1f}")
        c2.metric("Projeção de Cartões", f"{pred_amarelos:.1f}")
        c3.metric("Ambas Marcam", status_btts)
        
        st.info(f"Análise baseada no desempenho de 2025 aplicada aos confrontos de 2026.")
