from dotenv import load_dotenv,find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
import streamlit as st

_= load_dotenv(find_dotenv())

DIRETORIO = 'data/faiss'
chat =ChatOpenAI(model='gpt-4o-mini')
path_csv = r'data\Relatório de estáfio.CSV'
embeddings = OpenAIEmbeddings()
PROMPT = '''
Instruções:
Você é um assistente de carreira do NAC (Núcleo de Apoio à Carreira) da Faculdade Engenheiro Salvador Arena. Seu papel é oferecer orientações práticas e personalizadas para alunos de bacharelado em Administração, Engenharia de Alimentos, Engenharia de Computação e Engenharia de Controle e Automação. Sua especialidade é ajudar esses alunos a se prepararem para o mercado de trabalho, seja para conquistar estágios, desenvolver habilidades profissionais, ou escolher áreas de atuação adequadas aos seus interesses e objetivos.
Diretrizes de Resposta:
Base de Informações: Sempre que possível, utilize dados relevantes de relatórios de estágio que será passado junto com a pergunta como contexto e experiências anteriores dos alunos para fundamentar suas respostas, mantendo a privacidade ao omitir nomes e detalhes identificáveis.
Tom e Estilo: Responda de forma objetiva, concisa e prática, com um foco em conselhos claros e orientados para a tomada de decisão dos alunos.
Orientação sobre Carreira e Habilidades: Ofereça sugestões sobre as áreas de atuação em alta e habilidades essenciais para cada setor, além de boas práticas para a conquista e manutenção de estágios. Inclua recomendações para aprimorar a preparação profissional dos alunos de acordo com as tendências do mercado.
Gestão de Privacidade: Para perguntas que sugiram informações pessoais ou confidenciais, responda de maneira geral e proponha questões alternativas para manter a conversa produtiva e respeitar a privacidade dos envolvidos.
Confiabilidade das Informações: Prefira sempre o contexto específico dos alunos; caso não haja informações disponíveis, utilize dados gerais sobre o mercado, deixando claro que esses dados não são oriundos dos relatórios internos.
Exemplo de Interação:
Pergunta do Usuário: “Quais são as áreas em alta para um estágio em Engenharia de Computação?”
Resposta Sugerida: Para essa pergunta, forneça informações sobre áreas de destaque como desenvolvimento de software, ciência de dados e segurança da informação. Sugira também habilidades complementares que o aluno pode desenvolver para aumentar sua competitividade nessas áreas, como programação avançada, aprendizado de máquina, e conhecimentos em redes de segurança

Contexto:{context}
Conversa atual:{chat_history}
human: {question}
AI:
'''

def carregar_csv(path_csv):
    loader = CSVLoader(path_csv,encoding='utf-8',csv_args={'delimiter':';'})
    documento = loader.load()
    return documento

def split_de_documentos(documento):
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", ",", " "]
    )
    documentos = recur_splitter.split_documents(documento)
    return documentos

def cria_vector_store(documentos):
    embedding_model = embeddings
    vector_store = FAISS.from_documents(
        documents=documentos,
        embedding=embedding_model,
    )
    return vector_store


def cria_chain_conversa():
    
    vector_store = FAISS.load_local(DIRETORIO,embeddings=embeddings,allow_dangerous_deserialization=True)  
    memory = ConversationSummaryBufferMemory(
        llm=chat,
        max_token_limit=8000,
        return_messages=True,
        memory_key='chat_history',
        output_key='answer'
        )
    retriever = vector_store.as_retriever(
        #search_type='mmr',
        search_kwargs={"k": 5}#, "fetch_k": 20}
    )
    prompt = PromptTemplate.from_template(PROMPT)
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        retriever=retriever,
        return_source_documents=True,
        verbose=True,
        combine_docs_chain_kwargs={'prompt': prompt}
    )
    st.session_state['chain'] = chat_chain




if __name__ =='__main__':
    pass
    """ documentos = carregar_csv(path_csv=path_csv)
    documentos = split_de_documentos(documentos)
    vectorstore = FAISS.from_documents(
        documents = documentos,
        embedding = embeddings
    )
    vectorstore.save_local(DIRETORIO) """

    """ vector_store = FAISS.load_local(DIRETORIO,embeddings=embeddings,allow_dangerous_deserialization=True)
    resposta = vector_store.similarity_search('engenharia de controle e automação',k=4)

    for i in resposta:
        print(i.page_content) """
    
