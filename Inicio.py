import streamlit as st
import pandas as pd
import plotly.express as px
from database import criar_tabela_receitas, criar_tabela_despesas, adicionar_despesa, adicionar_receita
from filtros import obter_receitas_mes_atual, obter_despesas_mes_atual, obter_despesas_categorias
import os
import sqlite3

st.cache_data()

total_receitas = obter_receitas_mes_atual()
total_despesas = obter_despesas_mes_atual()

st.set_page_config(
    page_title="Dashboard Finanças",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title(":bar_chart: Dashboard Finanças")

st.subheader(' ')

criar_tabela_receitas()
criar_tabela_despesas()

# PRIMEIRA PARTE -> VISUALIZAÇÃO DOS DADOS PRINCIPAIS
col1, col2, col3= st.columns(3)

# BALANÇO
with col1:
    with st.container(height=180, border=True):
        balanco = total_receitas - total_despesas
        if balanco < 0 or balanco == 0:
            balanco = 0
        st.subheader('Balanço 🏦')
        st.metric(label="Saldo aproximado de todas contas", value=f"R${balanco:.2f}", delta="")

# RECEITAS
with col2:
    with st.container(height=180, border=True):
        if total_receitas < 0 or total_receitas == 0:
            total_receitas = 0
        st.subheader('Receita 💰')
        st.metric(label="Total de receitas desse mês", value=f"R${total_receitas:.2f}", delta="")

# DESPESAS
with col3:
    with st.container(height=180, border=True):
        if total_despesas < 0 or total_despesas == 0:
            total_despesas = 0
        st.subheader('Despesa 🪙')
        st.metric(label="Total de despesas desse mês", value=f"R${total_despesas:.2f}", delta="")

st.write(' ')

tra, cart, cont = st.columns(3)

with tra:
        # BOTÃO DE ADICIONAR RECEITAS E DESPESAS
    selection = st.radio("", ["Fechado", "Receitas", "Despesas"], horizontal=True, label_visibility="collapsed")

    # SEGUNDA PARTE -> ADICIONAR RECEITAS
    if selection == "Receitas":
        st.subheader("Adicionar Receitas")
        a, b = st.columns(2)
        with a:
            titulo_receita = st.text_input("Titulo").capitalize()
        with b:
            valor_receita = st.number_input("Valor", min_value=0.1, step=0.01)
        data_receita = st.date_input("Data").strftime('%Y-%m-%d')
        if st.button("Adicionar Receita"):
            try:
                adicionar_receita(titulo_receita, valor_receita, data_receita)
                st.success("Receita adicionada com sucesso!")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Erro ao adicionar receita: {str(e)}")

    # TERCEIRA PARTE -> ADICIONAR DESPESAS
    if selection == "Despesas":
        st.subheader("Adicionar Despesas")
        a, b = st.columns(2)
        with a:
            titulo_despesa = st.text_input("Titulo").capitalize()
        with b:
            valor_despesa = st.number_input("Valor", min_value=0.1, step=0.01)
        c, d = st.columns(2)
        with c:
            data_despesa = st.date_input("Data").strftime('%Y-%m-%d')
        with d:
            tipo_despesa = st.selectbox("Categoria", ["Entretenimento", "Transporte", "Alimentação", "Educação", "Casa", "Saúde", "Compras", "Investimento"])
        if st.button("Adicionar Despesa"):
            try:
                adicionar_despesa(titulo_despesa, valor_despesa, data_despesa, tipo_despesa)
                st.success("Despesa adicionada com sucesso!")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Erro ao adicionar despesa: {str(e)}")
with cart:
    st.write('')

with cont:
    st.write('')

st.write(' ')

pasta_projeto = os.getcwd()
caminho_db = os.path.join(pasta_projeto, 'despesas.db')

query = """
SELECT * FROM despesas
WHERE strftime('%Y-%m', data) = strftime('%Y-%m', DATE('now'))
"""

df = pd.read_sql_query(query, sqlite3.connect(caminho_db))

# Convertendo a coluna 'data' para o tipo datetime
# Convert data to datetime and sort
df['data'] = pd.to_datetime(df['data'])
df = df.sort_values('data')

# Group by date and category
daily_df = df.groupby([df['data'].dt.date, 'categoria'])['valor'].sum().reset_index()

fig = px.bar(
    daily_df,
    x="categoria",
    y="valor",
    color="categoria",
    title="Gastos Mensal por Categoria",
    labels={"valor": "Valor (R$)", "categoria": "Categoria"}
)

fig.update_layout(
    xaxis=dict(
        tickmode='auto',
        dtick='D1',  # Show tick for each day
        tickformat='%d/%m',  # Brazilian date format
    ),
    yaxis_tickprefix='R$ ',
    hovermode="x unified",
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02
    )
)

# Add hover template
fig.update_traces(
    hovertemplate="<br>".join([
        "Valor: R$ %{y:.2f}",
        "<extra></extra>"
    ])
)

st.plotly_chart(fig, use_container_width=True)