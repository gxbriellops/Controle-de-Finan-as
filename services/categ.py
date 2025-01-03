from dataclasses import dataclass
from typing import List
import streamlit as st
from decimal import Decimal

@dataclass
class Categoria:
    nome: str
    emoji: str
    orcamento_mensal: Decimal
    gasto_mensal: Decimal
    descricao: str

    @property
    def utilizacao(self) -> float:
        """Calcula a porcentagem de utilização do orçamento."""
        if self.gasto_mensal == 0:
            return 0.0
        return (self.gasto_mensal / self.orcamento_mensal) * 100

    def to_html(self) -> str:
        """Gera a representação HTML da categoria."""
        return f"""
            <h5 style="margin: 0;">{self.nome} {self.emoji}</h5>
            <p style="margin: 0;"><cite>{self.descricao}</cite></p>
            <p style="margin: 0;"><strong>Orçamento Mensal:</strong> R${self.orcamento_mensal:,.2f}</p>
            <p style="margin: 0;"><strong>Gasto Mensal:</strong> R${self.gasto_mensal:,.2f}</p>
            <p style="margin: 0;"><strong>Utilização:</strong> {self.utilizacao:.2f}%</p>
        """

def render_categoria(categoria: Categoria) -> None:
    """Renderiza uma categoria no Streamlit."""
    with st.container(height=180, border=True):
        st.markdown(categoria.to_html(), unsafe_allow_html=True)

# Dados das categorias
CATEGORIAS_DATA = [
    {
        "nome": "Entretenimento",
        "emoji": "🎉",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Lazer, Jogos, Cinema etc..."
    },
    {
        "nome": "Transporte",
        "emoji": "🚗",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Transporte, Viagem, Gasolina etc..."
    },
    {
        "nome": "Alimentação",
        "emoji": "🍔",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Mercado, Restaurante, Lanches etc..."
    },
    {
        "nome": "Educação",
        "emoji": "📚",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Cursos, Livros, Palestras etc..."
    },
    {
        "nome": "Casa",
        "emoji": "🏠",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Aluguel, Pet, Manutenção, Internet..."
    },
    {
        "nome": "Saúde",
        "emoji": "💊",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Farmácia, Consulta, Medicamentos, Autocuidado etc..."
    },
    {
        "nome": "Compras",
        "emoji": "👗",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Roupas, Sapatos, Acessórios, Eletronicos etc..."
    },
    {
        "nome": "Investimento",
        "emoji": "💰",
        "orcamento_mensal": Decimal("1000"),
        "gasto_mensal": Decimal("1000"),
        "descricao": "Investimentos, Poupança, Ações etc..."
    }
]

def main():
    categorias = [Categoria(**data) for data in CATEGORIAS_DATA]
    for categoria in categorias:
        render_categoria(categoria)

if __name__ == "__main__":
    main()