import pandas as pd
import streamlit as st
import sqlite3
import os

st.set_page_config(layout="wide")

st.title("Transações")

# Construir o caminho dos bancos de dados
base_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório atual do script
db_despesas_path = os.path.join(base_dir, "../despesas.db")

# Conectar aos bancos de dados SQLite
try:
    with sqlite3.connect(db_despesas_path) as conn_despesas:
        df_despesas = pd.read_sql_query("SELECT titulo, valor, data, categoria FROM despesas", conn_despesas)
except Exception as e:
    st.error(f"Erro ao acessar o banco de dados de despesas: {e}")
    df_despesas = pd.DataFrame()

# Converter a coluna 'data' para o formato de data (datetime)
df_despesas['data'] = pd.to_datetime(df_despesas['data'])

# Extrair o mês/ano em formato de período
df_despesas['mês'] = df_despesas['data'].dt.to_period('M')

# Agrupar por mês/ano e somar os valores numéricos
group = df_despesas.groupby('mês')

# Obter os meses disponíveis como uma lista formatada por extenso
mesesDisponiveis = df_despesas['mês'].dt.strftime("%B %Y").unique().tolist()

# Criação de colunas no layout do Streamlit
col1, col2 = st.columns(2)

with col1:
    st.subheader("Filtros")
    selection = st.selectbox(
        'Período de meses',
        options=mesesDisponiveis)  # Seleção padrão: do primeiro ao último mês

    # Filtrar o DataFrame com base nos meses selecionados
    df_despesas_filtrado = df_despesas[(df_despesas['mês'] == selection)]


with col2:
    st.subheader("Despesas")
    if not df_despesas.empty:
        st.data_editor(df_despesas_filtrado)
    else:
        st.info("Nenhuma despesa encontrada.")
