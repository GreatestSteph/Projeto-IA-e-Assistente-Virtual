# Código da Aplicação

Esta pasta contém o código do agente financeiro chamado NicoAI

## Estrutura

```
data/
├── perfil_investidor.json          # Dados
├── produtos_financeiros.json       # Dados
├── transacoes.csv                  # Dados
├── historico_atendimento.csv       # Dados
src/
├── app.py              # Aplicação principal (Streamlit)
```

## Dependências

```
streamlit
ollama
pandas
requests
```

## Como Rodar

```bash
# Instalar Ollama
ollama pull gpt-oss
ollama serve

# Instalar dependências
pip install streamlit pandas requests

# Rodar a aplicação NicoAI
streamlit run src/app.py
```
