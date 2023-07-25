import os
import sys

import constants
from langchain.document_loaders import TextLoader, WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = constants.APIKEY

if len(sys.argv) > 1:
    question = sys.argv[1]
else:
    print("Se debe indicar una pregunta.")
    sys.exit(1) 

from langchain.document_loaders import UnstructuredExcelLoader

# loader = TextLoader('data.txt', encoding='utf8')
# loader = UnstructuredExcelLoader("valia-qa.xlsx", mode="elements")
from langchain.document_loaders import Docx2txtLoader
loader = Docx2txtLoader('Valia-qa.docx',)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

# web_loader = WebBaseLoader("https://blog.valiapro.com/2-roles-esenciales-de-un-agente-inmobiliario-exitoso-0")
# index = VectorstoreIndexCreator().from_loaders([loader, web_loader])
# response = index.query(question, llm=ChatOpenAI())



#example with chroma
data = loader.load()

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)

# Store 
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

docs = vectorstore.similarity_search(question)


from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
# qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())
# result = qa_chain({"query": question})

#Retrieve response with question source citation
# qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=vectorstore.as_retriever())
# result = qa_chain({"question": question})

#use promt template
# Build prompt
from langchain.prompts import PromptTemplate
template = """Eres un chatbot asistente amistoso y educado. 
    Utilizando la informacion proporcionada. Responde siempre de manera clara, directa, y muy concisa. Cuando te pregunten sobre algo, 
    retorna el enlace correspondiente que más ayudará a responder la pregunta. 
    Por ejemplo si te preguntan "¿Como subo 
    una transacción?" responde "Aquí puedes ver un tutorial sobre como subir una transacción" y comparte el enlace correspondiente
    Genera la respuesta como un texto html, utilizando un <p> para el texto, un <a> para el enlace y <strong> para lo que consideres necesario
    {context}
    Pregunta: {question}
    Respuesta:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

# llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
# qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})

# result = qa_chain({"query": question})


from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

from langchain.chains import ConversationalRetrievalChain
chat = ConversationalRetrievalChain.from_llm(llm, retriever=vectorstore.as_retriever(), memory=memory)

result = chat({"question": question})

answer = result['answer']

print('result ---------------------------------------------------- ')
print(answer)

# print(response)