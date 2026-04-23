import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Analista Pro 2026", layout="wide")
st.title("🕵️ Web Scraper: Dados Reais 2025-2026")

# URL oficial de estatísticas
URL_STATS = "https://fbref.com/pt/comps/24/stats/Serie-A-Estatisticas"

@st.cache_data(ttl=3600)
def carregar_dados_com_disfarce():
    # Cabeçalho que simula um navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        # Primeiro baixamos o conteúdo com requests usando o disfarce
        response = requests.get(URL_STATS, headers=headers)
        if response.status_code == 403:
            return "Bloqueio 403: O site recusou o acesso. Tente novamente em alguns minutos."
        
        # O Pandas lê a tabela do texto baixado
        tabelas = pd.read_html(response.text)
        df = tabelas[0]
        
        # Limpeza de colunas (Série A FBRef tem cabeçalho duplo)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[1] for col in df.columns.values]
        
        return df
    except Exception as e:
        return f"Erro: {str(e)}"

if st.button('🔍 Extrair Dados Sem Bloqueio'):
    with st.spinner('Simulando acesso seguro...'):
        dados = carregar_dados_com_disfarce()
        
        if isinstance(dados, str):
            st.error(dados)
        else:
            st.success("Acesso autorizado! Dados carregados.")
            
            # Ajuste das colunas para o que você precisa
            # O FBRef usa 'Gls' para Gols e 'Squad' para Time
            st.subheader("📊 Performance Real da Temporada")
            colunas_ver = ['Squad', 'MP', 'Gls', 'Ast', 'CrdY']
            colunas_finais = [c for c in colunas_ver if c in dados.columns]
            
            if colunas_finais:
                df_exibir = dados[colunas_finais].copy()
                df_exibir.columns = ['Time', 'Jogos', 'Gols', 'Assist', 'Amarelos']
                st.dataframe(df_exibir, use_container_width=True)
            else:
                st.dataframe(dados.head(10))
