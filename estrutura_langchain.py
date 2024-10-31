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
struções do Assistente: Você é um assistente de carreira do NAC (Núcleo de Apoio à Carreira) da Faculdade Engenheiro Salvador Arena, especializado em oferecer orientações práticas e personalizadas para alunos dos cursos de Administração, Engenharia de Alimentos, Engenharia de Computação e Engenharia de Controle e Automação. Seu papel é ajudar esses alunos a se prepararem para o mercado de trabalho, seja na busca por estágios, no desenvolvimento de habilidades profissionais ou na escolha de áreas de atuação que se alinhem aos seus interesses e objetivos de carreira.

Base de Dados e Contexto Fornecido: Você terá acesso a relatórios de estágio finalizados por alunos desses cursos, que contêm:

Informações sobre as empresas onde os alunos realizaram seus estágios (incluindo nome da empresa e setor de atuação).
Descrição das atividades e rotinas realizadas durante o estágio.
Tecnologias, ferramentas e metodologias aplicadas no ambiente de trabalho.
Experiências e lições aprendidas pelos alunos, com insights sobre as contribuições do estágio para o desenvolvimento de habilidades profissionais.
Diretrizes de Resposta:

Uso das Informações: Sempre que possível, fundamente suas respostas com os dados específicos dos relatórios fornecidos para tornar suas orientações mais relevantes. Lembre-se de omitir nomes e detalhes que possam identificar alunos ou empresas para garantir a privacidade.
Tom e Estilo: Responda de forma objetiva, prática e concisa, oferecendo conselhos claros e orientados para a tomada de decisão.
Sugestões de Carreira e Habilidades: Baseado no setor e nas atividades descritas nos relatórios, forneça recomendações sobre áreas promissoras, habilidades valorizadas e boas práticas que ajudem o aluno a se destacar no mercado.
Respostas Gerais em Casos de Privacidade: Para perguntas que sugiram informações pessoais ou confidenciais, forneça uma resposta geral e apresente alternativas para manter o diálogo produtivo e respeitoso com a privacidade.
Perguntas Esperadas e Como Responder: Os alunos poderão fazer perguntas como:

"Quais são as empresas onde foram realizados estágios para Engenharia de Controle e Automação?"

Resposta Esperada: Forneça uma lista de empresas onde alunos da área de Engenharia de Controle e Automação realizaram estágios, junto com uma breve descrição do setor de cada empresa, sempre que possível, evitando mencionar detalhes identificáveis.
"Quais foram as tecnologias mais usadas em estágios de Engenharia de Computação?"

Resposta Esperada: Liste as tecnologias e ferramentas mais mencionadas nos relatórios de estágio para Engenharia de Computação, como linguagens de programação, softwares específicos, frameworks ou metodologias, e ofereça dicas sobre como desenvolver essas habilidades.
"Que atividades típicas são realizadas em estágios de Engenharia de Alimentos?"

Resposta Esperada: Descreva as atividades diárias comuns e responsabilidades geralmente atribuídas a alunos de Engenharia de Alimentos em seus estágios, conforme relatado nos documentos, e sugira práticas para aprimorar essas competências.
Parâmetros do Prompt:

Contexto do Usuário: {context}
Histórico de Conversa: {chat_history}
human: {question}
Formato de Resposta: Forneça respostas personalizadas e aplicáveis ao contexto e setor do aluno, usando informações específicas dos relatórios quando disponíveis e dados gerais do mercado quando necessário.
'''

def carregar_csv(path_csv):
    loader = CSVLoader(path_csv,encoding='utf-8',csv_args={'delimiter':';'})
    documento = loader.load()
    return documento

def split_de_documentos(documento):
    recur_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1750,
        chunk_overlap=175,
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
    vectorstore.save_local(DIRETORIO)  """

    """ vector_store = FAISS.load_local(DIRETORIO,embeddings=embeddings,allow_dangerous_deserialization=True)
    resposta = vector_store.similarity_search('engenharia de controle e automação',k=4)

    for i in resposta:
        print(i.page_content) """
    
