import os
import sqlite3

def obter_receitas_mes_atual():
    try:
        pasta_projeto = os.getcwd()
        caminho_db = os.path.join(pasta_projeto, 'receitas.db')
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        query = """
        SELECT SUM(valor) FROM receitas
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', DATE('now'));
        """
        cursor.execute(query)
        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado if resultado else 0.0
    except Exception as e:
        print(f"Erro ao obter receitas do mês atual: {str(e)}")
        return 0.0

def obter_despesas_mes_atual():
    try:
        pasta_projeto = os.getcwd()
        caminho_db = os.path.join(pasta_projeto, 'despesas.db')
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        query = """
        SELECT SUM(valor) FROM despesas
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', DATE('now'));
        """
        cursor.execute(query)
        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado if resultado else 0.0
    except Exception as e:
        print(f"Erro ao obter despesas do mês atual: {str(e)}")
        return 0.0
    
def obter_despesas_categorias(categoria: str):
    try:
        pasta_projeto = os.getcwd()
        caminho_db = os.path.join(pasta_projeto, 'despesas.db')
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        query = f"""
        SELECT SUM(valor) FROM despesas
        WHERE categoria = '{categoria}' = strftime('%Y-%m', DATE('now'));
        """
        cursor.execute(query)
        resultado = cursor.fetchone()[0]
        conn.close()
        return resultado if resultado else 0.0
    except Exception as e:
        print(f"Erro ao obter despesas do mês atual: {str(e)}")
        return 0.0