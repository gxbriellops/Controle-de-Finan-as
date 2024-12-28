import pandas as pd
import streamlit as st
import sqlite3
import os

st.set_page_config(layout="wide")

# Definir categorias permitidas
CATEGORIAS = [
    "Educação",
    "Investimento",
    "Compras",
    "Alimentação",
    "Transporte",
    "Entretenimento",
    "Casa",
    "Saúde"
]

# Função para atualizar o banco de dados
def update_transaction(conn, titulo, valor, data, categoria, original_titulo):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE despesas 
            SET titulo = ?, valor = ?, data = ?, categoria = ?
            WHERE titulo = ?
        """, (titulo, valor, data, categoria, original_titulo))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar transação: {e}")
        return False

# Função para normalizar valores para comparação
def normalize_value(value):
    if isinstance(value, float):
        return round(value, 2)
    return value

st.title("Transações")

# Construir o caminho dos bancos de dados
base_dir = os.path.dirname(os.path.abspath(__file__))
db_despesas_path = os.path.join(base_dir, "../despesas.db")

# Conectar ao banco de dados SQLite
try:
    conn_despesas = sqlite3.connect(db_despesas_path)
    df_despesas = pd.read_sql_query("SELECT titulo, valor, data, categoria FROM despesas", conn_despesas)
except Exception as e:
    st.error(f"Erro ao acessar o banco de dados de despesas: {e}")
    df_despesas = pd.DataFrame()

if not df_despesas.empty:
    # Converter a coluna 'data' para o formato datetime
    df_despesas['data'] = pd.to_datetime(df_despesas['data'])
    
    # Extrair o mês/ano em formato de período
    df_despesas['mês'] = df_despesas['data'].dt.to_period('M')
    
    # Obter os meses disponíveis e ordenar de forma decrescente
    meses_periodos = sorted(df_despesas['mês'].unique(), reverse=True)
    mesesDisponiveis = [mes.strftime("%B %Y") for mes in meses_periodos]
    

    st.subheader("Filtros")
    
    # Filtro de mês
    selection = st.selectbox(
        'Período de meses',
        options=mesesDisponiveis,
        index=0  # Selecionar o mês mais recente por padrão
    )
    
    # Filtrar o DataFrame com base nos meses selecionados e categorias
    df_despesas_filtrado = df_despesas[
        (df_despesas['mês'].dt.strftime("%B %Y") == selection)
    ]
    
    # Remover a coluna mês da visualização e resetar o índice
    df_display = df_despesas_filtrado.drop(columns=['mês']).reset_index(drop=True)
    
    # Inicializar o estado anterior se necessário
    if 'previous_data' not in st.session_state:
        st.session_state.previous_data = df_display.copy()
        st.session_state.previous_selection = selection
    
    # Configurar o editor de dados
    st.subheader("Despesas")
    
    # Configuração das colunas do editor
    config = {
        'titulo': st.column_config.TextColumn('Título'),
        'valor': st.column_config.NumberColumn(
            'Valor',
            min_value=0,
            format="R$ %.2f"
        ),
        'data': st.column_config.DateColumn(
            'Data',
            format="DD/MM/YYYY",
        ),
        'categoria': st.column_config.SelectboxColumn(
            'Categoria',
            options=CATEGORIAS,
            required=True
        )
    }
        
        # Criar o editor de dados
    if df_display.empty:
        st.info("Nenhuma despesa encontrada para os filtros selecionados.")
    else:
        edited_df = st.data_editor(
            df_display,
            column_config=config,
            key='transaction_editor',
            disabled=["titulo"]  # Desabilitar edição do título
        )
        
        # Verificar se o mês selecionado mudou
        if selection != st.session_state.previous_selection:
            st.session_state.previous_data = edited_df.copy()
            st.session_state.previous_selection = selection
        
        # Verificar se houve alterações reais
        elif edited_df is not None:
            for index, row in edited_df.iterrows():
                original_row = st.session_state.previous_data.loc[index]
                
                # Comparar valores normalizados
                row_changed = False
                for col in ['valor', 'data', 'categoria']:
                    if normalize_value(row[col]) != normalize_value(original_row[col]):
                        row_changed = True
                        break
                
                if row_changed:
                    # Converter o valor para número
                    valor_numerico = row['valor']
                    if isinstance(valor_numerico, str):
                        valor_numerico = float(valor_numerico.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    
                    # Atualizar no banco de dados
                    success = update_transaction(
                        conn_despesas,
                        row['titulo'],
                        valor_numerico,
                        row['data'].strftime('%Y-%m-%d'),
                        row['categoria'],
                        row['titulo']
                    )
                    
                    if success:
                        st.success(f"Transação '{row['titulo']}' atualizada com sucesso!")
            
            # Atualizar os dados anteriores
            st.session_state.previous_data = edited_df.copy()

else:
    st.info("Nenhuma despesa encontrada.")

# Fechar a conexão com o banco de dados
if 'conn_despesas' in locals():
    conn_despesas.close()