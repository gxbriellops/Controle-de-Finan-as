import pandas as pd
import streamlit as st
import sqlite3
import os

st.set_page_config(layout="wide")

st.title("Receitas")

# Construir o caminho dos bancos de dados
base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
db_receitas_path = os.path.join(base_dir, "../receitas.db")

# Conectar aos bancos de dados SQLite
try:
    with sqlite3.connect(db_receitas_path) as conn_receitas:
        df_receitas = pd.read_sql_query("SELECT titulo, valor, data, categoria FROM receitas", conn_receitas)
except Exception as e:
    st.error(f"Erro ao acessar o banco de dados de receitas: {e}")
    df_receitas = pd.DataFrame()

# Converter a coluna 'data' para o formato de data (datetime)
df_receitas['data'] = pd.to_datetime(df_receitas['data'])

# Extrair o mês/ano em formato de período
df_receitas['mês'] = df_receitas['data'].dt.to_period('M')

# Agrupar por mês/ano e somar os valores numéricos
group = df_receitas.groupby('mês')

# Obter os meses disponíveis como uma lista formatada por extenso
mesesDisponiveis = df_receitas['mês'].dt.strftime("%B %Y").unique().tolist()

# Criação de colunas no layout do Streamlit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Filtros")
    selection = st.selectbox(
        'Período de meses',
        options=mesesDisponiveis)  # Seleção padrão: do primeiro ao último mês

    # Filtrar o DataFrame com base nos meses selecionados
    df_receitas_filtrado = df_receitas[(df_receitas['mês'] == selection)]


with col2:
    st.subheader("Receitas")
    if not df_receitas.empty:
        st.data_editor(df_receitas_filtrado)
    else:
        st.info("Nenhuma despesa encontrada.")