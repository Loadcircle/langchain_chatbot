import os
import sys

import constants
from langchain.document_loaders import TextLoader, WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI

os.environ["OPENAI_API_KEY"] = constants.APIKEY

question = sys.argv[1]

loader = TextLoader('data.txt', encoding='utf8')
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.8)

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
vectorstore = Chroma.from_documents(documents=all_splits,embedding=OpenAIEmbeddings())

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
template = """Utiliza las siguientes pizas de contexto para responder a las pregunta, si no sabes una respuesta
    no trates de contestarla, tan solo responde: "no lo se", se conciso, con respuestas cortas de maximo 10 oraciones.
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

print('result ---------------------------------------------------- ')
print(result)

# print(response)