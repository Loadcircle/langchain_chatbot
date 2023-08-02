import os
import sys
import constants
import prompt
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

    
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Store 
embedding=OpenAIEmbeddings()
try:
    # Load from existing index
    vectorstore = Redis.from_existing_index(embedding=embedding, redis_url="redis://localhost:6379", index_name="valia_qa_2")

except:
    base_document_loader = Docx2txtLoader('data/Valia-qa.docx')
    base_document_data = base_document_loader.load()
    links_loader = WebBaseLoader(prompt.sources)
    links_data = links_loader.load()
    
    data = base_document_data + links_data

    #Split
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 50)
    all_splits = text_splitter.split_documents(data)
    vectorstore = Redis.from_documents(documents=all_splits, embedding=embedding, redis_url="redis://localhost:6379", index_name="valia_qa_2")

# results = vectorstore.similarity_search(question)

# Build prompt
template = prompt.template
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


# security prompt 

memoryHistory.append((question, answer))
guardar_memory_history()

print('----------------------------------------------------')
print(answer)
print('----------------------------------------------------')

print(type(result["source_documents"][0]))

# for i in result["source_documents"]:
    # print(i)
    # print('----------------------------------------------------')