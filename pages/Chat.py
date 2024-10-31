import streamlit as st
from estrutura_langchain import cria_chain_conversa
import time 

st.set_page_config(
    page_title='NAC Chatbot',
    page_icon='🤖',

)


if not 'chain' in st.session_state:
    cria_chain_conversa()
    st.rerun()

chain = st.session_state['chain']
memory = chain.memory
mensagens = memory.load_memory_variables({})['chat_history']
if 'curso' in st.session_state:   
    curso = st.session_state['curso']
else:
    curso = 'Engenharia de Controle e Automação'

cabecalho = "Inicie sua conversa" if len(mensagens) == 0 else 'Histórico da sua mensagem'
st.session_state['ver_botões'] = True if len(mensagens) == 0 else False


st.header(f'💬 {cabecalho}',divider=True)


def input_user(nova_mensagem):
    chat = st.chat_message('human',avatar= '🧑🏽‍🎓')
    chat.markdown(nova_mensagem)
    chat = st.chat_message('ai',avatar='🤖')
    chat.markdown('Gerando resposta')
    resposta = chain.invoke({'question': nova_mensagem})
    st.session_state['ultima_resposta'] = resposta
    st.rerun()




if st.session_state['ver_botões']:
    pergunta1 = f'Quais são as responsabilidades e rotina de diária de um estagiário do meu curso {curso} ?'
    pergunta2 = f'Quais habilidades ou conhecimentos específicos foram necessários para estágio em {curso} ?'
    pergunta3 = f'Quais foram os principais problemas ou desafios identificados no início do estágio de {curso} ?'
    pergunta4 = 'Como o projeto de estágio contribuiu para o desenvolvimento pessoal e profissional do estagiário?'
    pergunta5 = f'Quais empresas foram realizados os estágios de {curso}'
    btn1 = st.button(pergunta1)
    btn2 = st.button(pergunta2)
    btn3 = st.button(pergunta3)
    btn4 = st.button(pergunta4)
    btn5 = st.button(pergunta5)
    if btn1:
        pergunta = pergunta1
        input_user(pergunta)
    if btn2:
        pergunta = pergunta2
        input_user(pergunta)
    if btn3:
        pergunta = pergunta3
        input_user(pergunta)
    if btn4:
        pergunta = pergunta4
        input_user(pergunta)
    if btn5:
        pergunta  = pergunta5
        input_user(pergunta)
    
    if btn1 or btn2 or btn3 or btn4 or btn5:
        st.rerun()
    


nova_mensagem = st.chat_input('Faça sua pergunta...')

if nova_mensagem:
        chat = st.chat_message('human',avatar= '🧑🏽‍🎓')
        chat.markdown(nova_mensagem)
        chat = st.chat_message('ai',avatar='🤖')
        chat.markdown('Gerando resposta')
        resposta = chain.invoke({'question': nova_mensagem,'chat_history':mensagens})
        st.rerun()


for mensagem in mensagens:
    avatar = '🤖' if mensagem.type == 'ai' else '🧑🏽‍🎓'
    chat = st.chat_message(mensagem.type,avatar=avatar )
    chat.markdown(mensagem.content)