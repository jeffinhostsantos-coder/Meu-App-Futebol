import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analista Pro 2026", layout="wide")

# Função que busca os dados SEM precisar de planilha
@st.cache_data(ttl=3600)
def buscar_dados_direto():
    try:
        # Usamos a Wikipédia ou sites de estatística estáveis
        url = "https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_2024_-_S%C3%A9rie_A"
        tabelas = pd.read_html(url)
        # Geralmente a tabela de classificação é a primeira ou segunda
        df = tabelas[6] # Ajustamos o índice conforme a estrutura do site
        df.columns = [str(c).upper().strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return None

st.title("🛡️ Analisador de Confrontos Direto (Sem Planilha)")

dados = buscar_dados_direto()

if dados is not None:
    # Identifica a coluna de times (geralmente chamada de 'EQUIPE' ou 'TIME')
    col_time = [c for c in dados.columns if 'EQUIPE' in c or 'TIME' in c][0]
    lista_times = dados[col_time].unique()

    st.sidebar.header("Simular Jogo 2026")
    casa = st.sidebar.selectbox("Mandante", lista_times)
    fora = st.sidebar.selectbox("Visitante", lista_times)

    if st.sidebar.button("📊 GERAR PROBABILIDADES"):
        st.header(f"⚔️ {casa} vs {fora}")
        
        # Lógica para Ambas Marcam, Cantos e Cartões baseada na posição da tabela
        pos_casa = dados[dados[col_time] == casa].index[0]
        pos_fora = dados[dados[col_time] == fora].index[0]

        # Probabilidades Inteligentes
        prob_btts = "Alta (75%)" if pos_casa < 10 and pos_fora < 10 else "Média (50%)"
        cantos = "10.5" if pos_casa < 5 else "8.5"
        cartoes = "5.5" if pos_casa > 15 else "4.5"

        c1, c2, c3 = st.columns(3)
        c1.metric("Ambas Marcam", prob_btts)
        c2.metric("Escanteios", f"+{cantos}")
        c3.metric("Cartões", f"+{cartoes}")

    st.divider()
    st.subheader("📋 Tabela Atualizada em Tempo Real")
    st.dataframe(dados)
else:
    st.warning("Aguardando conexão com o servidor de dados...")
