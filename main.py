import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Preditor Pro 2026", layout="wide")

# Link da sua planilha CSV
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4oAQdRvnyDmqozRSX2wggU8ABqruw2LgD8P0mKqsLkYCe8CC14jeSKpZ6Q5IaAHjLKPlgdqXp0wPE/pub?output=csv"

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        return None

def calcular_probabilidades(casa, fora, df):
    dados_casa = df[df['Time'] == casa].iloc[0]
    dados_fora = df[df['Time'] == fora].iloc[0]
    
    # Lógica de Predição (Baseada em médias e peso de 5 jogos)
    prob_vitoria = "Empate/Equilibrado"
    if (dados_casa['Vitórias'] > dados_fora['Vitórias'] + 3):
        prob_vitoria = casa
    elif (dados_fora['Vitórias'] > dados_casa['Vitórias'] + 3):
        prob_vitoria = fora
        
    # Ambas Marcam (BTTS)
    btts_casa = float(str(dados_casa['Ambas Marcam (BTTS)']).replace('%',''))
    btts_fora = float(str(dados_fora['Ambas Marcam (BTTS)']).replace('%',''))
    btts_final = "Sim" if (btts_casa + btts_fora) / 2 > 55 else "Não"
    
    return {
        "vencedor": prob_vitoria,
        "btts": btts_final,
        "escanteios": round((dados_casa['Escanteios (Média)'] + dados_fora['Escanteios (Média)']), 1),
        "cartoes": round((dados_casa['Cartões (Média)'] + dados_fora['Cartões (Média)']) / 2, 1)
    }

st.title("🤖 Analista Preditivo: Brasileirão 2026")
dados = carregar_dados()

if dados is not None:
    # --- Seção de Confronto Futuro ---
    st.header("🔮 Simulador de Próximos Confrontos")
    col_c, col_f = st.columns(2)
    
    with col_c:
        time_casa = st.selectbox("Mandante", dados['Time'].unique(), index=0)
    with col_f:
        time_fora = st.selectbox("Visitante", dados['Time'].unique(), index=1)
    
    if st.button("🔥 Gerar Aposta Sugerida"):
        res = calcular_probabilidades(time_casa, time_fora, dados)
        
        st.success(f"**Análise Concluída para {time_casa} vs {time_fora}**")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Provável Vencedor", res['vencedor'])
        c2.metric("Ambas Marcam", res['btts'])
        c3.metric("Linha de Cantos", f"+ {res['escanteios']}")
        c4.metric("Média de Cartões", res['cartões'])
        
        st.warning(f"💡 **Dica de Aposta:** Entrada sugerida em Over {res['escanteios'] - 1.5} cantos e BTTS {res['btts']}.")

    st.markdown("---")
    st.subheader("📊 Base de Dados (Últimos 5 Jogos)")
    st.dataframe(dados, use_container_width=True, hide_index=True)
else:
    st.error("Erro ao carregar dados. Verifique a publicação da planilha.")
