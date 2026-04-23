import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Analista Pro Fut", layout="wide")
st.title("⚽ Dashboard de Análise Inteligente")

api_key = 'c9f55dc0e91ac61caf1e05371daa9a8c'
headers = {'x-rapidapi-key': api_key}

st.sidebar.header("Configurações")
ano_selecionado = st.sidebar.selectbox("Temporada para Análise", [2026, 2025, 2024])

# Lista expandida de times
times_ids = {
    "Flamengo": 127, "Palmeiras": 121, "Botafogo": 120, "São Paulo": 126, 
    "Bahia": 118, "Internacional": 119, "Atlético-MG": 106, "Fortaleza": 154, 
    "Cruzeiro": 131, "Corinthians": 117, "Vasco": 133, "Fluminense": 124
}

if st.button(f'🚀 Analisar Temporada {ano_selecionado}'):
    dados_finais = []
    progresso = st.progress(0)
    placeholder = st.empty() # Para mensagens de status
    
    for i, (nome, tid) in enumerate(times_ids.items()):
        placeholder.text(f"Consultando: {nome}...")
        
        # Tentativa de buscar estatísticas
        url = f"https://v3.football.api-sports.io/teams/statistics?league=71&season={ano_selecionado}&team={tid}"
        response = requests.get(url, headers=headers).json()
        
        res = response.get('response')
        
        # Se a API retornar dados, processamos. Se não, pulamos para o próximo.
        if res and res.get('fixtures', {}).get('played', {}).get('total', 0) > 0:
            escanteios = res.get('corners', {}).get('avg', {}).get('total', 0) or 0
            amarelos = res.get('cards', {}).get('yellow', {}).get('total', 0) or 0
            gols_f = res.get('goals', {}).get('for', {}).get('average', {}).get('total', 0) or 0
            gols_s = res.get('goals', {}).get('against', {}).get('average', {}).get('total', 0) or 0
            
            btts = "✅ ALTA" if float(gols_f) > 1.0 and float(gols_s) > 0.8 else "❌ BAIXA"
            
            dados_finais.append({
                "Time": nome,
                "Escanteios (Média)": float(escanteios),
                "Cartões Amarelos": amarelos,
                "Tendência AMBAS": btts,
                "Vitórias": res.get('fixtures', {}).get('wins', {}).get('total', 0)
            })
        
        progresso.progress((i + 1) / len(times_ids))
    
    placeholder.empty()

    if dados_finais:
        df = pd.DataFrame(dados_finais)
        st.subheader(f"📊 Resultados encontrados para {ano_selecionado}")
        st.dataframe(df.sort_values(by='Escanteios (Média)', ascending=False))
    else:
        st.warning(f"⚠️ A API ainda não tem estatísticas calculadas para a temporada {ano_selecionado}. Tente selecionar 2025 ou 2024 para ver o histórico dos times.")
