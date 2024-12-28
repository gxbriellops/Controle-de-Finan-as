import pandas as pd
import streamlit as st
import sqlite3
import os

# Definir categorias de receitas
Categorias = [
    'Salário mensal',
    'Freelance',
    'Renda passiva'
]

def update_receita(conn, titulo, valor, data, categoria, original_titulo):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE receitas 
            SET titulo = ?, valor = ?, data = ?, categoria = ?
            WHERE titulo = ?
        """, (titulo, valor, data, categoria, original_titulo))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar receita: {e}")
        return False

# Função para normalizar valores para comparação
def normalize_value(value):
    if isinstance(value, float):
        return round(value, 2)
    return value

st.set_page_config(layout="wide")

st.title("Receitas")

# Construir o caminho dos bancos de dados
base_dir = os.path.dirname(os.path.abspath(__file__))
db_receitas_path = os.path.join(base_dir, "../receitas.db")

# Conectar ao banco de dados SQLite
try:
    conn_receitas = sqlite3.connect(db_receitas_path)
    df_receitas = pd.read_sql_query("SELECT titulo, valor, data, categoria FROM receitas", conn_receitas)
except Exception as e:
    st.error(f"Erro ao acessar o banco de dados de receitas: {e}")
    df_receitas = pd.DataFrame()

if not df_receitas.empty:
    # Converter a coluna 'data' para o formato datetime
    df_receitas['data'] = pd.to_datetime(df_receitas['data'])
    
    # Extrair o mês/ano em formato de período
    df_receitas['mês'] = df_receitas['data'].dt.to_period('M')
    
    # Obter os meses disponíveis e ordenar de forma decrescente
    meses_periodos = sorted(df_receitas['mês'].unique(), reverse=True)
    mesesDisponiveis = [mes.strftime("%B %Y") for mes in meses_periodos]
    
    st.subheader("Filtros")
    
    # Filtro de mês
    selection = st.selectbox(
        'Período de meses',
        options=mesesDisponiveis,
        index=0  # Selecionar o mês mais recente por padrão
    )
    
    # Filtrar o DataFrame com base nos meses selecionados e categorias
    df_receitas_filtrado = df_receitas[
        (df_receitas['mês'].dt.strftime("%B %Y") == selection)
    ]
    
    # Remover a coluna mês da visualização e resetar o índice
    df_display = df_receitas_filtrado.drop(columns=['mês']).reset_index(drop=True)
    
    # Inicializar o estado anterior se necessário
    if 'previous_data' not in st.session_state:
        st.session_state.previous_data = df_display.copy()
        st.session_state.previous_selection = selection
    
    # Configurar o editor de dados
    st.subheader("Receitas")
    
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
            options=Categorias,
            required=True
        )
    }
    
    # Criar o editor de dados
    if df_display.empty:
        st.info("Nenhuma receita encontrada para os filtros selecionados.")
    else:
        edited_df = st.data_editor(
            df_display,
            column_config=config,
            key='receitas_editor',
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
                    success = update_receita(
                        conn_receitas,
                        row['titulo'],
                        valor_numerico,
                        row['data'].strftime('%Y-%m-%d'),
                        row['categoria'],
                        row['titulo']
                    )
                    
                    if success:
                        st.success(f"Receita '{row['titulo']}' atualizada com sucesso!")
            
            # Atualizar os dados anteriores
            st.session_state.previous_data = edited_df.copy()

else:
    st.info("Nenhuma receita encontrada.")

# Fechar a conexão com o banco de dados
if 'conn_receitas' in locals():
    conn_receitas.close()