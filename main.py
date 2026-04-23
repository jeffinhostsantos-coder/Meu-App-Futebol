import streamlit as st
import requests
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Analista Pro Fut", layout="wide")
st.title("⚽ Painel de Análise Estatística")

# Sua Chave API
api_key = 'c9f55dc0e91ac61caf1e05371daa9a8c'
headers = {'x-rapidapi-key': api_key}

# IDs dos times do Brasileirão (IDs Reais da API)
times_ids = {
    "Flamengo": 127, "Palmeiras": 121, "Botafogo": 120, 
    "São Paulo": 126, "Bahia": 118, "Internacional": 119,
    "Atlético-MG": 106, "Fortaleza": 154, "Cruzeiro": 131, "Corinthians": 131
}

if st.button('🚀 Gerar Relatório de Oportunidades'):
    dados_finais = []
    progresso = st.progress(0)
    
    for i, (nome, tid) in enumerate(times_ids.items()):
        # Usando a temporada 2024 para garantir que existam dados estatísticos
        url = f"https://v3.football.api-sports.io/teams/statistics?league=71&season=2024&team={tid}"
        
        try:
            response = requests.get(url, headers=headers)
            res = response.json()['response']
            
            # Extração segura dos dados
            escanteios = res.get('corners', {}).get('avg', {}).get('total', 0) or 0
            amarelos = res.get('cards', {}).get('yellow', {}).get('total', 0) or 0
            gols_feitos = res.get('goals', {}).get('for', {}).get('average', {}).get('total', 0) or 0
            gols_sofridos = res.get('goals', {}).get('against', {}).get('average', {}).get('total', 0) or 0
            vitorias = res.get('fixtures', {}).get('wins', {}).get('total', 0) or 0
            
            # Lógica de Ambas Marcam
            btts_vibe = "✅ ALTA" if float(gols_feitos) > 1.0 and float(gols_sofridos) > 0.9 else "❌ BAIXA"
            
            dados_finais.append({
                "Time": nome,
                "Escanteios (Média)": float(escanteios),
                "Cartões Amarelos": amarelos,
                "Tendência AMBAS": btts_vibe,
                "Vitórias": vitorias
            })
        except Exception as e:
            st.error(f"Erro ao buscar dados do {nome}")
            
        progresso.progress((i + 1) / len(times_ids))

    if dados_finais:
        df = pd.DataFrame(dados_finais)
        
        # Rankings
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔥 Top Escanteios")
            st.dataframe(df[['Time', 'Escanteios (Média)']].sort_values(by='Escanteios (Média)', ascending=False))
            
        with col2:
            st.subheader("🟨 Top Cartões")
            st.dataframe(df[['Time', 'Cartões Amarelos']].sort_values(by='Cartões Amarelos', ascending=False))
            
        st.subheader("📊 Analise de Ambas Marcam (BTTS)")
        st.table(df[['Time', 'Tendência AMBAS', 'Vitórias']])
    else:
        st.warning("Nenhum dado encontrado. Verifique sua chave API.")
