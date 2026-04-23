import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analista Pro Série A", layout="wide")

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4oAQdRvnyDmqozRSX2wggU8ABqruw2LgD8P0mKqsLkYCe8CC14jeSKpZ6Q5IaAHjLKPlgdqXp0wPE/pub?output=csv"

@st.cache_data(ttl=600)
def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        df.columns = [c.strip().upper() for c in df.columns]
        # Resolve o KeyError: busca qualquer coluna que pareça ser o nome do time
        col_time = [c for c in df.columns if c in ['TIME', 'EQUIPE', 'EQUIPES', 'SQUAD']][0]
        df = df.rename(columns={col_time: 'NOME_TIME'})
        return df
    except:
        return None

st.title("🎯 Preditor Série A: Confrontos Futuros")
dados = carregar_dados()

if dados is not None:
    st.sidebar.header("Próximo Jogo (26/04/2026)")
    casa = st.sidebar.selectbox("Mandante", dados['NOME_TIME'].unique())
    fora = st.sidebar.selectbox("Visitante", dados['NOME_TIME'].unique())

    if st.sidebar.button("📊 Calcular Probabilidades"):
        d_casa = dados[dados['NOME_TIME'] == casa].iloc[0]
        d_fora = dados[dados['NOME_TIME'] == fora].iloc[0]

        st.header(f"⚔️ {casa} vs {fora}")
        
        # --- LÓGICA DE ÚLTIMOS 5 JOGOS ---
        # Conta vitórias na coluna 'ÚLT_5' ou 'FORMA' da ESPN
        forma_casa = str(d_casa.get('ÚLT_5', 'V')).count('V')
        forma_fora = str(d_fora.get('ÚLT_5', 'V')).count('V')

        # Ambas Marcam (BTTS): Baseado em Gols Pró (GP) > 1.2
        prob_btts = "ALTA (78%)" if (float(d_casa.get('GP', 0)) > 1.2 and float(d_fora.get('GP', 0)) > 1.0) else "BAIXA (42%)"
        
        # Escanteios e Cartões
        cantos = 10.5 if (forma_casa + forma_fora) > 5 else 8.5
        cartoes = "+4.5" if forma_casa < 2 else "+3.5"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Vencedor Provável", casa if forma_casa >= forma_fora else fora)
        c2.metric("Ambas Marcam", prob_btts)
        c3.metric("Linha de Cantos", f"+{cantos}")
        c4.metric("Risco de Cartões", cartoes)

        st.info(f"💡 **Dica Profissional:** Jogo com tendência de {prob_btts} para Ambas Marcam e vantagem para o {casa if forma_casa >= forma_fora else fora} pela forma recente.")

    st.divider()
    st.dataframe(dados, use_container_width=True)
else:
    st.error("Erro ao carregar banco de dados. Verifique a publicação do Google Sheets.")
