import streamlit as st
import pandas as pd
import plotly.express as px
from services.database import criar_tabela_receitas, criar_tabela_despesas, adicionar_despesa, adicionar_receita
from services.filtros import obter_receitas_mes_atual, obter_despesas_mes_atual
import os
import sqlite3

st.cache_data()

total_receitas = obter_receitas_mes_atual()
total_despesas = obter_despesas_mes_atual()


slidebar = 'assets/imagens/logo bold.png'
icon = 'assets/imagens/simbolol bold.png'

st.logo(slidebar, icon_image=icon, size='large')

st.set_page_config(
    page_title="Mínimo",
    layout="wide"
)

st.title("Início")

st.subheader(' ')

criar_tabela_receitas()
criar_tabela_despesas()

# PRIMEIRA PARTE -> VISUALIZAÇÃO DOS DADOS PRINCIPAIS
col1, col2, col3= st.columns(3)

# BALANÇO
with col1:
    balanco = pd.DataFrame({'Tipo': ['Receitas', 'Despesas'], 'Valor':[total_receitas, total_despesas]})
    pie = px.pie(balanco, values='Valor', names='Tipo', title='Balanço', color_discrete_sequence=['green', 'red'])
    pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    st.plotly_chart(pie)

# RECEITAS
with col2:
    with st.container(height=180, border=True):
        if total_receitas < 0 or total_receitas == 0:
            total_receitas = 0
        st.subheader('Entradas 💰')
        st.metric(label="Total de receitas desse mês", value=f"R${total_receitas:.2f}", delta="")
    st.subheader("Nova entrada")
    a, b = st.columns(2)
    with a:
        titulo_receita = st.text_input("Titulo da entrada").capitalize()
    with b:
        valor_receita = st.number_input("Valor da entrada", min_value=0.0, step=0.01)
    data_receita = st.date_input("Data da entrada").strftime('%Y-%m-%d')
    if st.button("Adicionar entrada"):
        try:
            adicionar_receita(titulo_receita, valor_receita, data_receita)
            st.success("Receita adicionada com sucesso!")
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Erro ao adicionar receita: {str(e)}")

# DESPESAS
with col3:
    with st.container(height=180, border=True):
        if total_despesas < 0 or total_despesas == 0:
            total_despesas = 0
        st.subheader('Gastos 🪙')
        st.metric(label="Total de gastos desse mês", value=f"R${total_despesas:.2f}", delta="")
    st.subheader("Adicionar gasto")
    a, b = st.columns(2)
    with a:
        titulo_despesa = st.text_input("Titulo da gasto").capitalize()
    with b:
        valor_despesa = st.number_input("Valor do gasto", min_value=0.0, step=0.01)
    c, d = st.columns(2)
    with c:
        data_despesa = st.date_input("Data da gasto").strftime('%Y-%m-%d')
    with d:
        tipo_despesa = st.selectbox("Categoria", ["Entretenimento", "Transporte", "Alimentação", "Educação", "Casa", "Saúde", "Compras", "Investimento"])
    if st.button("Adicionar gasto"):
        try:
            adicionar_despesa(titulo_despesa, valor_despesa, data_despesa, tipo_despesa)
            st.success("Gasto adicionado com sucesso!")
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Erro ao adicionar gasto: {str(e)}")

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