import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analista de Confrontos", layout="wide")

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4oAQdRvnyDmqozRSX2wggU8ABqruw2LgD8P0mKqsLkYCe8CC14jeSKpZ6Q5IaAHjLKPlgdqXp0wPE/pub?output=csv"

@st.cache_data(ttl=300)
def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        # Padroniza nomes de colunas (remove espaços e deixa em maiúsculo)
        df.columns = [c.strip().upper() for c in df.columns]
        
        # Tenta encontrar a coluna de times independente do nome
        possiveis_nomes = ['TIME', 'EQUIPE', 'SQUAD', 'TEAM']
        for nome in possiveis_nomes:
            if nome in df.columns:
                df = df.rename(columns={nome: 'NOME_TIME'})
                break
        return df
    except:
        return None

st.title("⚽ Simulador de Confrontos 2025/2026")
dados = carregar_dados()

if dados is not None and 'NOME_TIME' in dados.columns:
    st.sidebar.header("Próximo Jogo")
    # Agora ele usa a coluna correta, evitando o erro do print
    casa = st.sidebar.selectbox("Mandante", dados['NOME_TIME'].unique())
    fora = st.sidebar.selectbox("Visitante", dados['NOME_TIME'].unique())

    if st.sidebar.button("Analisar Confronto"):
        d_casa = dados[dados['NOME_TIME'] == casa].iloc[0]
        d_fora = dados[dados['NOME_TIME'] == fora].iloc[0]
        
        st.header(f"⚔️ {casa} vs {fora}")
        
        # Exemplo de lógica para "Ambas Marcam" e "Escanteios" baseada nos times
        col1, col2, col3 = st.columns(3)
        with col1:
            # Se o time faz muitos gols e sofre muitos, tendência de BTTS Sim
            st.metric("Tendência Ambas Marcam", "ALTA" if d_casa.get('GOLS', 0) > 1 else "MÉDIA")
        with col2:
            st.metric("Projeção de Cantos", f"+{round(d_casa.get('ESCANTARIOS (MÉDIA)', 5) + d_fora.get('ESCANTARIOS (MÉDIA)', 5) - 1, 1)}")
        with col3:
            st.metric("Favorito", casa if d_casa.get('VITÓRIAS', 0) > d_fora.get('VITÓRIAS', 0) else fora)

    st.divider()
    st.subheader("📋 Tabela Atualizada de Times")
    st.dataframe(dados, use_container_width=True)
else:
    st.error("Erro: A coluna de 'Time' não foi encontrada. Verifique o cabeçalho da sua planilha.")
