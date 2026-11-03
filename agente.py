import os
import streamlit as st
from openai import AzureOpenAI

# Configuração da página
st.set_page_config(
    page_title="Professor de Música IA - Azure",
    page_icon="🎵",
    layout="centered"
)

# Título e descrição
st.title("🎵 Maestro.IA - Seu Professor de Música (Azure)")
st.markdown("Tire dúvidas de teoria musical, aprenda escalas, acordes e receba dicas de prática via Azure Foundry!")

# Configuração da barra lateral para credenciais da Azure
with st.sidebar:
    st.header("⚙️ Configurações Azure OpenAI")
    azure_endpoint = st.text_input("Azure Endpoint URL:", placeholder="https://seu-recurso.openai.azure.com/")
    api_key_input = st.text_input("Azure API Key:", type="password")
    deployment_name = st.text_input("Deployment Name (Nome do Modelo):", value="gpt-4o")
    api_version = st.text_input("API Version:", value="2024-02-01-preview")
    
    st.markdown("---")
    st.markdown("### 🎸 Sobre o Agente")
    st.markdown("Agente pedagógico musical rodando com a infraestrutura corporativa da Azure.")

# Verificar se as credenciais foram preenchidas
if not api_key_input or not azure_endpoint or not deployment_name:
    st.warning("⚠️ Por favor, preencha o Endpoint, a API Key e o Deployment Name na barra lateral para iniciar.")
    st.stop()

# Inicializar o cliente Azure OpenAI
try:
    client = AzureOpenAI(
        api_key=api_key_input,
        api_version=api_version,
        azure_endpoint=azure_endpoint
    )
except Exception as e:
    st.error(f"Erro ao configurar o cliente Azure: {e}")
    st.stop()

# Definir o System Prompt (COSTAR)
SYSTEM_PROMPT = """
Você é um professor de música experiente, apaixonado, paciente e altamente didático, especializado em ensinar teoria musical, harmonia, prática de instrumentos e composição. 
Explique conceitos de forma clara, sugira exercícios práticos e utilize um tom amigável, acolhedor e encorajador.
"""

# Histórico de mensagens no chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# Exibir histórico de mensagens
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Ex: Como faço para montar um acorde de Dó Maior?"):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gerar resposta via Azure OpenAI
    try:
        with st.chat_message("assistant"):
            with st.spinner("Pensando na melodia (Azure)..."):
                response = client.chat.completions.create(
                    model=deployment_name,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    temperature=0.7,
                    max_tokens=1024,
                )
                assistant_response = response.choices[0].message.content
                st.markdown(assistant_response)
                
        # Adicionar resposta ao histórico
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        
    except Exception as e:
        st.error(f"Ocorreu um erro ao comunicar com a API da Azure: {e}")