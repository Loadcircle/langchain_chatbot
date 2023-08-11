import os
import sys
import constants
import prompt_variables
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import Docx2txtLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores.redis import Redis

os.environ["OPENAI_API_KEY"] = constants.APIKEY

try:
    from memory_history import memoryHistory
except ImportError:
    memoryHistory = []

if len(sys.argv) > 1:
    question = sys.argv[1]
else:
    print("Se debe indicar una pregunta.")
    sys.exit(1) 


def guardar_memory_history():
    # Guardar la variable memoryHistory en el archivo memory_history.py
    with open('memory_history.py', 'w', encoding='utf-8') as file:
        file.write(f"memoryHistory = {memoryHistory}")

if question == "refresh":
    print("Memoria eliminada")
    memoryHistory = []
    guardar_memory_history()
    sys.exit(1) 


def run_qa(question):        
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Store 
    embedding=OpenAIEmbeddings()
    try:
        # Load from existing index
        vectorstore = Redis.from_existing_index(embedding=embedding, redis_url="redis://localhost:6379", index_name="valia_qa_2")

    except:
        base_document_loader = Docx2txtLoader('data/Valia-qa.docx')
        base_document_data = base_document_loader.load()
        links_loader = WebBaseLoader(prompt_variables.link_sources)
        links_data = links_loader.load()
        
        data = base_document_data + links_data

        #Split
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 50)
        all_splits = text_splitter.split_documents(data)
        vectorstore = Redis.from_documents(documents=all_splits, embedding=embedding, redis_url="redis://localhost:6379", index_name="valia_qa_2")

    # results = vectorstore.similarity_search(question)

    # Build prompt
    template = prompt_variables.template
    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

    #set previous memory history
    chat_history = []
    for input, output in memoryHistory:
        chat_history.append((input, output))

    chain_kwargs = {
        "prompt": QA_CHAIN_PROMPT,
    }

    #we can use any form of memory, either passing to the conversationalretrieval or to the chat param
    
    chat = ConversationalRetrievalChain.from_llm(llm, retriever=vectorstore.as_retriever(), combine_docs_chain_kwargs=chain_kwargs, return_source_documents = True)

    result = chat({"question": question, "chat_history": chat_history})

    answer = result['answer']

    try:
        source = result["source_documents"][0].metadata['source']
    except (KeyError, TypeError):
        print("Error", KeyError, TypeError)
        source = None
    
    response = {
        "question": question,
        "answer": answer,
        "source": source
    }

    security_response = security_model(response, vectorstore)

    return security_response

from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

def get_link(question):    
    llm = ChatOpenAI(temperature=0)
    
    #links format for the model 
    sources = [f"<<{p['source']}>>: {p['description']}" for p in prompt_variables.sources]
    
    sources_str = "\n".join(sources)

    validator_template = prompt_variables.link_validator_template.format(
        sources=sources_str
    )

    prompt = ChatPromptTemplate.from_template(validator_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    
    chat_response = chain.run(question)

    if chat_response == 'NONE':
        return None
    else:
        return chat_response

from langchain.chains import RetrievalQA
def security_model(response, vectorstore):

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    template = prompt_variables.validator_template
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template=template)

    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
    
    result = qa_chain({"query": response["answer"]})

    response["security_answer"] = result["result"]
    
    return response


def run(question):

    response = run_qa(question)
    validator_source = get_link(question)

    answer = response["security_answer"]

    memoryHistory.append((question, answer))
    guardar_memory_history()

    if validator_source is not None:
        answer += "\n\nPuedes encontrar más información en el siguiente enlace:\n" + validator_source

    print(answer)

    exit()

run(question)













#APPRAISAL
