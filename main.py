import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analista Pro 2026", layout="wide")
st.title("🎯 Analisador de Dados (GE & ESPN Edition)")

# COLE O SEU LINK DO GOOGLE SHEETS (CSV) ABAIXO:
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4oAQdRvnyDmqozRSX2wggU8ABqruw2LgD8P0mKqsLkYCe8CC14jeSKpZ6Q5IaAHjLKPlgdqXp0wPE/pub?output=csv"

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        # Lógica para ler a planilha sem erros
        df = pd.read_csv(URL_PLANILHA)
        return df
    except:
        # Se você ainda não colou o link, ele mostra dados de exemplo
        data = {
            'Time': ['Flamengo', 'Palmeiras', 'São Paulo'],
            'Cantos (GE)': [6.5, 5.9, 5.1],
            'Cartões (ESPN)': [2.2, 3.1, 1.9],
            'Fonte': ['ge.globo', 'espn.com', 'google.com']
        }
        return pd.DataFrame(data)

st.sidebar.header("Filtros do Analista")
if st.sidebar.button("🔄 Atualizar Dados"):
    st.cache_data.clear()
    st.rerun()

dados = carregar_dados()

# Interface do Usuário
st.subheader("📊 Estatísticas Cruzadas (Fontes Abertas)")
st.dataframe(dados, use_container_width=True)

if "Cantos (GE)" in dados.columns:
    st.subheader("🔥 Tendência de Escanteios")
    st.bar_chart(dados.set_index('Time')['Cantos (GE)'])
