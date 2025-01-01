import sqlite3
import os
from datetime import datetime

def criar_tabela_receitas():
    # Obter o caminho atual do projeto
    pasta_projeto = os.getcwd()
    caminho_db = os.path.join(pasta_projeto, 'receitas.db')

    # Conexão com o banco de dados (cria o arquivo receitas.db na pasta do projeto)
    conn = sqlite3.connect(caminho_db)

    # Criação do cursor para executar comandos SQL
    cursor = conn.cursor()

    # Comando SQL para criar a tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        valor REAL NOT NULL,
        data DATE NOT NULL
    );
    """

    # Executar o comando SQL
    cursor.execute(create_table_query)

    # Confirmar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

def criar_tabela_despesas():
    # Obter o caminho atual do projeto
    pasta_projeto = os.getcwd()
    caminho_db = os.path.join(pasta_projeto, 'despesas.db')

    # Conexão com o banco de dados (cria o arquivo receitas.db na pasta do projeto)
    conn = sqlite3.connect(caminho_db)

    # Criação do cursor para executar comandos SQL
    cursor = conn.cursor()

    # Comando SQL para criar a tabela
    create_table_query = """
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        valor REAL NOT NULL,
        data DATE NOT NULL,
        categoria TEXT NOT NULL
    );
    """

    # Executar o comando SQL
    cursor.execute(create_table_query)

    # Confirmar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

def adicionar_receita(titulo, valor, data):
    try:
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        datetime.strptime(data, '%Y-%m-%d')  # Valida o formato da data
        pasta_projeto = os.getcwd()
        caminho_db = os.path.join(pasta_projeto, 'receitas.db')
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        query = """
        INSERT INTO receitas (titulo, valor, data)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (titulo, valor, data))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao adicionar receita: {str(e)}")
        return False

def adicionar_despesa(titulo, valor, data, categoria):
    try:
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        datetime.strptime(data, '%Y-%m-%d')  # Valida o formato da data
        pasta_projeto = os.getcwd()
        caminho_db = os.path.join(pasta_projeto, 'despesas.db')
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        query = """
        INSERT INTO despesas (titulo, valor, data, categoria)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (titulo, valor, data, categoria))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao adicionar despesa: {str(e)}")
        return False