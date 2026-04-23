import streamlit as st
import pandas as pd

st.set_page_config(page_title="Analista Master 2026", layout="wide")

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4oAQdRvnyDmqozRSX2wggU8ABqruw2LgD8P0mKqsLkYCe8CC14jeSKpZ6Q5IaAHjLKPlgdqXp0wPE/pub?output=csv"

@st.cache_data(ttl=300)
def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        df.columns = [c.strip().upper() for c in df.columns]
        # Resolve o erro de 'Time' procurando o nome da coluna correto da ESPN
        col_time = [c for c in df.columns if 'EQUIPE' in c or 'TIME' in c or 'SQUAD' in c][0]
        df = df.rename(columns={col_time: 'NOME_TIME'})
        return df
    except:
        return None

st.title("⚽ Preditor de Confrontos: Brasileirão 2026")
dados = carregar_dados()

if dados is not None:
    st.sidebar.header("Próximos Jogos (Abril/2026)")
    time_casa = st.sidebar.selectbox("Mandante", dados['NOME_TIME'].unique())
    time_fora = st.sidebar.selectbox("Visitante", dados['NOME_TIME'].unique())

    if st.sidebar.button("📊 GERAR ANÁLISE PREDITIVA"):
        d_casa = dados[dados['NOME_TIME'] == time_casa].iloc[0]
        d_fora = dados[dados['NOME_TIME'] == time_fora].iloc[0]

        st.subheader(f"⚔️ Análise: {time_casa} vs {time_fora}")
        
        # --- LÓGICA DE ÚLTIMOS 5 JOGOS ---
        # Analisa a coluna 'ÚLT_5' que vem da ESPN (V-E-D)
        vitorias_casa = str(d_casa.get('ÚLT_5', 'E')).count('V')
        vitorias_fora = str(d_fora.get('ÚLT_5', 'E')).count('V')

        # Ambas Marcam: Se a média de gols pró (GP) for alta em ambos
        prob_btts = "ALTA (80%)" if (float(d_casa.get('GP', 0)) > 1.2 and float(d_fora.get('GP', 0)) > 1.0) else "BAIXA (45%)"
        
        # Escanteios e Cartões: Baseado na agressividade ofensiva (Forma Recente)
        est_cantos = 10.5 if (vitorias_casa + vitorias_fora) > 5 else 8.5
        est_cartoes = "+4.5" if vitorias_casa < 2 else "+3.5"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Vencedor Provável", time_casa if vitorias_casa >= vitorias_fora else time_fora)
        c2.metric("Ambas Marcam", prob_btts)
        c3.metric("Escanteios", f"+{est_cantos}")
        c4.metric("Cartões", est_cartoes)

        st.success(f"💡 **Prognóstico:** Jogo com tendência de {prob_btts} Ambas Marcam e vantagem para o {time_casa if vitorias_casa >= vitorias_fora else time_fora}.")

    st.divider()
    st.write("### 📋 Tabela Geral de Times (Sincronizada GE/ESPN)")
    st.dataframe(dados, use_container_width=True)
else:
    st.error("Erro ao carregar dados. Verifique a publicação CSV da sua planilha.")
