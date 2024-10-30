import streamlit as st 

st.set_page_config(
    page_title='NAC Chatbot',
    page_icon='🤖',
)



st.header('🤖 NAC Chatbot: Chatbot de auxílio a carreira profissional',divider=True)
st.session_state['curso'] = st.selectbox('Selecione seu curso',('Administração','Engenharia de alimentos','Engenharia de computação','Engenharia de controle e automação'))

st.markdown('''\n\n
Estou aqui para te ajudar a questonamentos sobre carreira, com base nas experiências de alunos que já realizaram estágio.
Fui alimentado com extensos relatórios de estágios finalizados, as informações que possuo:
### Introdução
Contém o contexto do projeto, incluindo os problemas ou desafios que o projeto pretende resolver, também esboça os objetivos do projeto e a abordagem ou metodologia utilizada para alcança-lós.
Os detalhes que seguirão e destacar a importância do projeto dentro de um contexto mais amplo.
### Caracterização da Empresa
Fornece uma visão abrangente da empresa ou do contexto no qual o estágio ou projeto foi realizado. Incluindo:
\nIdentificação da Empresa: Nome, localização, e informações de contato.\n
Histórico: Breve história da empresa e seu desenvolvimento ao longo do tempo.
### Área de Estágio
Descreve especificamente a área de foco do estágio, incluindo:\n
Descrição da Rotina: Atividades diárias e responsabilidades do estagiário.
### Conclusão
A conclusão contém os resultados do projeto, refletindo sobre o sucesso e as lições aprendidas.
Deve também destaca como o projeto contribuiu para o desenvolvimento pessoal e profissional do estagiário e o potencial de aplicação dos resultados na empresa em projetos futuros.
## Como posso ajudar? Aqui estão algumas coisas que posso fazer:
### Orientação de Carreira Baseada em Casos Reais:
O chatbot pode fornecer orientações sobre carreira utilizando exemplos concretos de desafios enfrentados e superados durante estágios anteriores. Isso inclui como os estagiários abordaram problemas específicos e quais metodologias utilizaram para alcançar seus objetivos.
### Entendimento Contextual dos Projetos:    
Oferecer informações detalhadas sobre diversas empresas, incluindo a história, desenvolvimento ao longo do tempo, e detalhes específicos como localização e informações de contato. Isso pode ajudar você a selecionar potenciais empregadores com base em seus interesses e alinhamento de carreira.
### Descrição das Rotinas de Estágio
Descrever as rotinas diárias e responsabilidades típicas de estagiários em diferentes áreas, proporcionando uma visão clara do que esperar em termos de carga de trabalho e tipos de tarefas a serem realizadas.
### Análise de Resultados e Sucesso do Projeto:
Analisar os resultados e o sucesso dos projetos de estágio, destacando as principais lições aprendidas e como esses aprendizados contribuíram para o desenvolvimento pessoal e profissional dos estagiários.
### Preparação para Futuros Projetos e Estágios:
Preparar você para futuros projetos e estágios, fornecendo uma base de conhecimento que eles podem levar adiante em suas carreiras, baseada em exemplos reais e práticos.
            
                       
''')