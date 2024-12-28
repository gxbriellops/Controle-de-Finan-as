import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from database import criar_tabela_receitas, criar_tabela_despesas, adicionar_despesa, adicionar_receita
from filtros import obter_receitas_mes_atual, obter_despesas_mes_atual, obter_despesas_categorias
from categ import Categoria, render_categoria
from decimal import Decimal

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
            data_despesa = st.date_input("Data").strftime('%d-%m-%Y')
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

# EXIBINDO AS COLUNAS DE CATEGORIAS

st.subheader("Categorias de Despesas")

options = ["Cartão", "Gráfico", "Orçamento"]
selection = st.radio("Selecionar uma opção", options=options, horizontal=True)

st.write(' ')
# FILTRANDO AS DESPESAS POR CATEGORIA NO MES ATUAL
if selection == "Gráfico":
    st.write('Em breve!')

if selection == "Orçamento":
    col1, col2 = st.columns(2)
    with col1:
        selectOrçamento = st.selectbox('Selecione a categoria', ['Alimentação', 'Saúde', 'Transporte', 'Entretenimento', 'Compras', 'Investimento', 'Casa', 'Educação'])
    with col2:
        if selectOrçamento == 'Alimentação':
            orAlimentacao = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)
        if selectOrçamento == 'Saúde':
            orSaude = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)
        if selectOrçamento == 'Transporte':
            orTransporte = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)
        if selectOrçamento == 'Entretenimento':
            orEntretenimento = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)
        if selectOrçamento == 'Compras':
            orCompras = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)
        if selectOrçamento == 'Investimento':
            orInvestimento = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)
        if selectOrçamento == 'Casa':
            orCasa = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)
        if selectOrçamento == 'Educação':
            orEdu = st.number_input('Digite o valor do orçamento', min_value=0.0, step=0.01)


if selection == "Cartão":

    despAlimentação = obter_despesas_categorias("Alimentação")
    despTransporte = obter_despesas_categorias("Transporte")
    despEntretenimento = obter_despesas_categorias("Entretenimento")
    despEducacao = obter_despesas_categorias("Educação")
    despCasa = obter_despesas_categorias("Casa")
    despSaude = obter_despesas_categorias("Saúde")
    despCompras = obter_despesas_categorias("Compras")
    despInvestimento = obter_despesas_categorias("Investimento")

    # DEFININDO OS DADOS DAS CATEGORIAS

    categorias = [
        Categoria(nome="Entretenimento", emoji="🎉", orcamento_mensal=Decimal("1000.00"),
                gasto_mensal=Decimal(despEntretenimento), descricao="Streaming, jogos, passeios."),
        Categoria(nome="Transporte", emoji="🚗", orcamento_mensal=Decimal("500.00"),
                gasto_mensal=Decimal(despEntretenimento), descricao="Transportes, estacionamento, gasolina."),
        Categoria(nome="Alimentação", emoji="🍔", orcamento_mensal=Decimal("800.00"),
                gasto_mensal=Decimal(despAlimentação), descricao="Restaurantes, fastfoods, mercado."),
        Categoria(nome="Educação", emoji="📚", orcamento_mensal=Decimal("600.00"),
                gasto_mensal=Decimal(despEducacao), descricao="Mensalidades, cursos, livros."),
        Categoria(nome="Casa", emoji="🏠", orcamento_mensal=Decimal("1200.00"),
                gasto_mensal=Decimal(despCasa), descricao="Contas de casa, pet."),
        Categoria(nome="Saúde", emoji="🏥", orcamento_mensal=Decimal("400.00"),
                gasto_mensal=Decimal(despSaude), descricao="Consultas, rémedios, autocuidado."),
        Categoria(nome="Compras", emoji="🛒", orcamento_mensal=Decimal("700.00"),
                gasto_mensal=Decimal(despCompras), descricao="Roupas, eletrônicos, acessórios."),
        Categoria(nome="Investimento", emoji="💹", orcamento_mensal=Decimal("900.00"),
                gasto_mensal=Decimal(despInvestimento), descricao="Ações, poupança, investimentos.")
    ]

    row1 = st.columns(4)
    row2= st.columns(4)

    # EXIBINDO AS COLUNAS DE CATEGORIAS

    for categoria, rol in zip(categorias, row1 + row2):
        with rol:
            render_categoria(categoria)