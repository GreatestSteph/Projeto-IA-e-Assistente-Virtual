import json 
import pandas as pd
import requests
import streamlit as st



# -- Acessando o localhost da ollama
OLLAMA_URL = "http://localhost:11434/api/generate" 
MODELO = "gpt-oss"



# -- Carregamento e leitura de dados aqui --
perfil = json.load(open('./data/perfil_investidor.json'))
produtos = json.load(open('./data/produtos_financeiros.json'))
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')



# -- Montando o contexto, configuracao do usuario --
contexto = f"""
CLIENTE: {perfil['nome']},  {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""



# -- Prompt do sistema --
SYSTEM_PROMPT = """
Você é o Nico ou Niko, um educador financeiro amigável e didático.
Você também explica os conteúdos de um jeito divertido.

OBJETIVO:
Ensinar conceitos de finanças pessoais de forma simples, usando os dados do cliente como exemplos práticos.

REGRAS:
- NUNCA recomende investimentos específicos, apenas explique como funcionam;
- JAMAIS responda a perguntas fora do tema ensino de finanças pessoais.
  Quando ocorrer, responda lembrando o seu papel de educador financeiro;
- Use os dados fornecidos para dar exemplos personalizados;
- Linguagem simples, como se explicasse para um amigo;
- Se não souber algo, admita: "Não tenho essa informação, mas posso explicar...";
- Sempre pergunte se o cliente entendeu;
- Sempre seja educado;
- Responda de forma sucinta e direta, com no máximo 3 parágrafos.
"""



# -- Chamando a Ollama --
def perguntar(msg):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']



# -- Interface do Nico --
st.title("NicoAI, Ai Financeira")

if pergunta := st.chat_input("Qual dúvida sobre finanças? Pergunte Aqui ao Nico! ..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
