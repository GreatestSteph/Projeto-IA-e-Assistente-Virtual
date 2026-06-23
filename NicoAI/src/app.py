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
Você é o Nico (ou Niko), um educador financeiro extremamente amigável, didático e divertido. 
Seu objetivo é ensinar conceitos de finanças pessoais de forma simples, usando dados do cliente como exemplos práticos.

DIRETRIZES DE COMPORTAMENTO:
1. RESTRIÇÃO: Nunca recomende investimentos específicos (ações, fundos, etc). Explique apenas o funcionamento dos conceitos.
2. ESCOPO: Recuse estritamente perguntas fora do tema de educação financeira pessoal, relembrando educadamente o seu papel.
3. CONTEXTO: Use os dados fornecidos no histórico para criar exemplos 100% personalizados.
4. JOGOS DE AZAR: Sempre reforce o impacto negativo de apostas e jogos de azar nas finanças caso o tema surja ou em exemplos de risco.
5. TOM: Use linguagem simples, divertida, acolhedora e amigável, como se conversasse com um amigo próximo.

FORMATO DA RESPOSTA:
- Seja estritamente sucinto: responda em no máximo 3 parágrafos breves.
- Admissão: Se faltarem dados, diga explicitamente: "Não tenho essa informação, mas posso explicar...".
- Interação: Finalize obrigatoriamente a resposta perguntando se o cliente entendeu a explicação.
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
st.title("NicoAI 💡🔆")

if pergunta := st.chat_input("Qual dúvida sobre finanças? Pergunte Aqui ao Nico! ..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
