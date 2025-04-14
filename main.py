# Importar as bibliotecas

import streamlit as st
import pandas as pd
import yfinance

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

lista_acoes = st.multiselect("Escolha as ações para visualização", dados.columns)
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})
    
        


# Criar o gráfico
st.line_chart(dados)
