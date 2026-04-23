import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Analista Pro 2026", layout="wide")

# Link da sua planilha (Já atualizado)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR4oAQdRvnyDmqozRSX2wggU8ABqruw2LgD8P0mKqsLkYCe8CC14jeSKpZ6Q5IaAHjLKPlgdqXp0wPE/pub?output=csv"

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        df = pd.read_csv(URL_PLANILHA)
        # Limpa espaços extras nos nomes das colunas
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        return f"Erro ao conectar com a planilha: {e}"

# --- Interface Principal ---
st.title("🎯 Dashboard de Análise: Brasileirão 2026")
st.markdown("---")

dados = carregar_dados()

if isinstance(dados, str):
    st.error(dados)
    st.info("Verifique se a planilha está publicada como CSV no Google Sheets.")
else:
    # Sidebar para filtros
    st.sidebar.header("Configurações")
    if st.sidebar.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()
    
    clube_selecionado = st.sidebar.selectbox("Filtrar por Clube", ["Todos"] + list(dados['Time'].unique()))

    # Filtro de dados
    df_filtrado = dados if clube_selecionado == "Todos" else dados[dados['Time'] == clube_selecionado]

    # Exibição de Métricas em Destaque
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Clubes", len(dados))
    with col2:
        if "Escanteios (Média)" in dados.columns:
            st.metric("Maior Média de Cantos", f"{dados['Escanteios (Média)'].max()}")
    with col3:
        st.write("**Fonte Ativa:** Google Sheets ✅")

    # Tabela Principal
    st.subheader("📊 Tabela Geral de Estatísticas")
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

    # Gráficos de Tendência
    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        if "Escanteios (Média)" in dados.columns:
            st.subheader("🔥 Rank de Escanteios")
            st.bar_chart(dados.set_index('Time')['Escanteios (Média)'])

    with col_b:
        if "Cartões (Média)" in dados.columns:
            st.subheader("🟨 Rank de Cartões Amarelos")
            st.bar_chart(dados.set_index('Time')['Cartões (Média)'])

    # Nota de rodapé
    st.caption("Nota: Alimente sua planilha no Google Sheets para atualizar os valores aqui instantaneamente.")
