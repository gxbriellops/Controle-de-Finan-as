import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from database import criar_tabela_receitas, criar_tabela_despesas, adicionar_despesa, adicionar_receita
from filtros import obter_receitas_mes_atual, obter_despesas_mes_atual

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
    # Inicializar a variável de estado
    if 'mostrar_formulario' not in st.session_state:
        st.session_state.mostrar_formulario = False

    # Botão para exibir o formulário
    if st.button("Adicionar Transação"):
        st.session_state.mostrar_formulario = True

    # Exibir o formulário se a variável de estado estiver True
    if st.session_state.mostrar_formulario:

        # BOTÃO DE ADICIONAR RECEITAS E DESPESAS
        selection = st.selectbox("Selecione o que você deseja adicionar:", ["Receitas", "Despesas"])

        # SEGUNDA PARTE -> ADICIONAR RECEITAS
        if selection == "Receitas":
            st.subheader("Adicionar Receitas")
            a, b = st.columns(2)
            with a:
                titulo_receita = st.text_input("Titulo").capitalize()
            with b:
                valor_receita = st.number_input("Valor", min_value=0.1, step=0.01)
            c, d = st.columns(2)
            with c:
                data_receita = st.date_input("Data").strftime('%Y-%m-%d')
            with d:
                tipo_receita = st.selectbox("Categoria", ["Salário mensal", "Freelance", "Renda passiva"])
            if st.button("Adicionar Receita"):
                if adicionar_receita(titulo_receita, valor_receita, data_receita, tipo_receita):
                    st.success("Receita adicionada com sucesso!")
                else:
                    st.error("Erro ao adicionar receita.")

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
                if adicionar_despesa(titulo_despesa, valor_despesa, data_despesa, tipo_despesa):
                    st.success("Despesa adicionada com sucesso!")
                else:
                    st.error("Erro ao adicionar despesa.")

with cart:
    
    if st.button('Meus cartões'):
        st.write('Em breve!')

with cont:
    if st.button('Contas'):
        st.write('Em breve!')

st.subheader(' ')

st.subheader("Categorias de Despesas")

st.write(' ')

cat1, cat2, cat3, cat4 = st.columns(4)
cat5, cat6, cat7, cat8 = st.columns(4)

st.header('Teste')