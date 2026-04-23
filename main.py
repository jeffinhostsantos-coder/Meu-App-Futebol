import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scraper Pro Fut", layout="wide")
st.title("🕵️ Web Scraper: Estatísticas Reais 2025-2026")

# URL do FBRef (Tabela de estatísticas do Brasileirão)
# O FBRef é excelente porque as URLs são fáceis de ler
URL_STATS = "https://fbref.com/pt/comps/24/stats/Serie-A-Estatisticas"

@st.cache_data(ttl=3600) # Guarda os dados por 1 hora para não ser bloqueado pelo site
def carregar_dados_scraping():
    try:
        # O Pandas lê todas as tabelas da página de uma vez
        tabelas = pd.read_html(URL_STATS)
        df = tabelas[0] # Geralmente a primeira tabela é a de estatísticas
        
        # Limpeza de colunas (FBRef usa níveis múltiplos)
        df.columns = [' '.join(col).strip() for col in df.columns.values]
        
        # Selecionando o que importa para você
        # Nota: Os nomes das colunas podem variar, então filtramos o que contém palavras-chave
        colunas_uteis = [c for c in df.columns if 'Squad' in c or 'Gls' in c or 'Ast' in c or 'Cartões Amarelos' in c]
        return df[colunas_uteis].head(20)
    except Exception as e:
        return f"Erro ao acessar o site: {e}"

st.sidebar.info("Este plano lê dados diretamente do FBRef via Web Scraping.")

if st.button('🔍 Extrair Dados Atualizados'):
    with st.spinner('O Python está lendo o site de estatísticas...'):
        df_stats = carregar_dados_scraping()
        
        if isinstance(df_stats, str):
            st.error(df_stats)
            st.warning("O site pode ter bloqueado o acesso temporário. Tente novamente em instantes.")
        else:
            st.success("Dados extraídos com sucesso!")
            
            # Ajuste de nomes para exibição
            df_stats.columns = ['Time', 'Gols', 'Assistências', 'Amarelos']
            
            # Criando métricas de assertividade
            st.subheader("📊 Tabela de Desempenho Real")
            st.dataframe(df_stats, use_container_width=True)
            
            st.divider()
            
            # Lógica de predição baseada no Scraping
            st.subheader("💡 Insight do Analista")
            top_gols = df_stats.sort_values(by='Gols', ascending=False).iloc[0]
            st.write(f"O time com maior tendência de gols atualmente é o **{top_gols['Time']}**.")
