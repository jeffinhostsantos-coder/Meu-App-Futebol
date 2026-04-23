import streamlit as st
import requests
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Analista Pro Fut", layout="wide")
st.title("⚽ Dashboard de Análise: 2025 vs 2026")

# Chave API
api_key = 'c9f55dc0e91ac61caf1e05371daa9a8c'
headers = {'x-rapidapi-key': api_key}

# Menu Lateral para escolha da Temporada
st.sidebar.header("Configurações de Análise")
ano_selecionado = st.sidebar.selectbox("Escolha a Temporada", [2026, 2025, 2024])

# Lista de IDs corrigida do Brasileirão
times_ids = {
    "Flamengo": 127, "Palmeiras": 121, "Botafogo": 120, 
    "São Paulo": 126, "Bahia": 118, "Internacional": 119,
    "Atlético-MG": 106, "Fortaleza": 154, "Cruzeiro": 131, "Corinthians": 117,
    "Vasco": 133, "Fluminense": 124, "Grêmio": 130, "Bragantino": 128
}

if st.button(f'🚀 Analisar Temporada {ano_selecionado}'):
    dados_finais = []
    progresso = st.progress(0)
    
    for i, (nome, tid) in enumerate(times_ids.items()):
        # URL dinâmica baseada no ano selecionado
        url = f"https://v3.football.api-sports.io/teams/statistics?league=71&season={ano_selecionado}&team={tid}"
        
        try:
            res = requests.get(url, headers=headers).json()['response']
            
            # Puxando dados com tratamento para não vir 0 se houver informação
            escanteios = res.get('corners', {}).get('avg', {}).get('total', 0) or 0
            amarelos = res.get('cards', {}).get('yellow', {}).get('total', 0) or 0
            gols_feitos = res.get('goals', {}).get('for', {}).get('average', {}).get('total', 0) or 0
            gols_sofridos = res.get('goals', {}).get('against', {}).get('average', {}).get('total', 0) or 0
            
            # Lógica de Ambas Marcam (BTTS)
            # Se faz mais de 1 gol e sofre mais de 0.8, a tendência é ALTA
            if float(gols_feitos) > 1.0 and float(gols_sofridos) > 0.8:
                btts = "✅ ALTA"
            else:
                btts = "❌ BAIXA"
            
            dados_finais.append({
                "Time": nome,
                "Escanteios (Média)": float(escanteios),
                "Amarelos (Média)": float(amarelos) / 10 if float(amarelos) > 20 else float(amarelos), # Ajuste de escala
                "Tendência AMBAS": btts,
                "Gols Pró/Jogo": float(gols_feitos)
            })
        except:
            continue
            
        progresso.progress((i + 1) / len(times_ids))

    if dados_finais:
        df = pd.DataFrame(dados_finais)
        
        # Dashboard Visual
        c1, c2 = st.columns(2)
        with c1:
            st.subheader(f"🔥 Top Escanteios - {ano_selecionado}")
            st.dataframe(df[['Time', 'Escanteios (Média)']].sort_values(by='Escanteios (Média)', ascending=False))
        with c2:
            st.subheader(f"🟨 Top Cartões Amarelos - {ano_selecionado}")
            st.dataframe(df[['Time', 'Amarelos (Média)']].sort_values(by='Amarelos (Média)', ascending=False))
            
        st.subheader("📊 Probabilidade de Ambas Marcam (BTTS)")
        st.table(df[['Time', 'Tendência AMBAS', 'Gols Pró/Jogo']])
    else:
        st.error("Dados não encontrados para esta temporada na API gratuita.")
