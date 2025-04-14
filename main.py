# Importar as bibliotecas

import streamlit as st
import pandas as pd
import yfinance
from datetime import timedelta

# criar funções de carregamento de dados
    # cotação do Itau (ITUB4) 2010 a 2024

@st.cache_data # informações da função abaixo vão ficar armazendas em cachê e sempre que for possível   
def carregar_dados(empresas):
    text_tickers = " ".join(empresas)
    dados_acao = yfinance.Tickers(text_tickers)
    cotacao_acoes = dados_acao.history(period='1d', 
                    start='2010-01-01', end='2025-01-01')
    cotacao_acoes = cotacao_acoes["Close"]
    return cotacao_acoes

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]   
dados = carregar_dados(acoes)
   

# criar a interface do streamlit 
st.write('''
         # App Preço de Ações
         O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
         ''') # markdown

# preparar visualizações  = filtros 

# Criar uma sidebar

st.sidebar.header("Filtros")


# Filtro de ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualização", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

# Filtro de datas
data_inicial = dados.index.min().to_pydatetime()
data_final = dados.index.max().to_pydatetime()

intervalo_data = st.sidebar.slider("Selecione o Período", 
                                    min_value= data_inicial , 
                                    max_value= data_final, 
                                    value= (data_inicial, data_final),
                                    step=timedelta(days=1))

dados = dados.loc[intervalo_data[0]: intervalo_data[1]]


        
# Criar o gráfico
st.line_chart(dados)
