import pandas as pd
import streamlit as st
import sqlite3
import os

slidebar = 'assets/imagens/logo extended.png'
icon = 'assets/imagens/logo.png'

st.set_page_config(
    page_title="Gastos",
    page_icon=icon,
    layout="wide"
)

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

def delete_transaction(conn, titulo):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM despesas WHERE titulo = ?
        """, (titulo,))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao excluir transação: {e}")
        return False

def normalize_value(value):
    if isinstance(value, float):
        return round(value, 2)
    return value

st.title("Gastos")

base_dir = os.path.dirname(os.path.abspath(__file__))
db_despesas_path = os.path.join(base_dir, "../despesas.db")

try:
    conn_despesas = sqlite3.connect(db_despesas_path)
    df_despesas = pd.read_sql_query("SELECT titulo, valor, data, categoria FROM despesas", conn_despesas)
except Exception as e:
    st.error(f"Erro ao acessar o banco de dados de despesas: {e}")
    df_despesas = pd.DataFrame()

if not df_despesas.empty:
    df_despesas['data'] = pd.to_datetime(df_despesas['data'])
    df_despesas['mês'] = df_despesas['data'].dt.to_period('M')
    
    meses_periodos = sorted(df_despesas['mês'].unique(), reverse=True)
    mesesDisponiveis = [mes.strftime("%B %Y") for mes in meses_periodos]

    st.subheader("Filtros")
    
    selection = st.selectbox(
        'Quando',
        options=mesesDisponiveis,
        index=0
    )
    
    df_despesas_filtrado = df_despesas[
        (df_despesas['mês'].dt.strftime("%B %Y") == selection)
    ]
    
    # Usar o título como índice para garantir consistência
    df_display = df_despesas_filtrado.drop(columns=['mês']).set_index('titulo')
    
    # Inicializar o estado anterior usando o título como chave
    if 'previous_data' not in st.session_state:
        st.session_state.previous_data = df_display.copy()
        st.session_state.previous_selection = selection
    
    st.subheader("Histórico de gastos")
    
    config = {
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
    
    if df_display.empty:
        st.info("Nenhuma despesa encontrada para os filtros selecionados.")
    else:
        df_display['ações'] = False

        edited_df = st.data_editor(
                df_display,
                column_config={
                    **config,
                    'ações': st.column_config.CheckboxColumn(
                        'Excluir',
                        help='Selecione para excluir a transação'
                    )
                },
                key='transaction_editor'
            )
        
        if st.button('Excluir selecionados'):
            titulos_exluir = edited_df[edited_df['ações']].index.tolist()
            if titulos_exluir:
                for titulo in titulos_exluir:
                    if delete_transaction(conn_despesas, titulo):
                        st.success(f"Transação '{titulo}' excluída com sucesso!")
                    else:
                        st.error(f"Erro ao excluir transação '{titulo}'")
        
        # Verificar se o mês selecionado mudou
        if selection != st.session_state.previous_selection:
            st.session_state.previous_data = edited_df.copy()
            st.session_state.previous_selection = selection
        
        elif edited_df is not None:
            for titulo in edited_df.index:
                if titulo in st.session_state.previous_data.index:
                    row = edited_df.loc[titulo]
                    original_row = st.session_state.previous_data.loc[titulo]
                    
                    row_changed = False
                    for col in ['valor', 'data', 'categoria']:
                        if normalize_value(row[col]) != normalize_value(original_row[col]):
                            row_changed = True
                            break
                    
                    if row_changed:
                        valor_numerico = row['valor']
                        if isinstance(valor_numerico, str):
                            valor_numerico = float(valor_numerico.replace('R$', '').replace('.', '').replace(',', '.').strip())
                        
                        success = update_transaction(
                            conn_despesas,
                            titulo,
                            valor_numerico,
                            row['data'].strftime('%Y-%m-%d'),
                            row['categoria'],
                            titulo
                        )
                        
                        if success:
                            st.success(f"Transação '{titulo}' atualizada com sucesso!")
            
            st.session_state.previous_data = edited_df.copy()

else:
    st.info("Nenhuma despesa encontrada.")

if 'conn_despesas' in locals():
    conn_despesas.close()