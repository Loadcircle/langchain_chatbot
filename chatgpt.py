import os
import sys

import constants
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import Docx2txtLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

os.environ["OPENAI_API_KEY"] = constants.APIKEY

if len(sys.argv) > 1:
    question = sys.argv[1]
else:
    print("Se debe indicar una pregunta.")
    sys.exit(1) 

loader = Docx2txtLoader('Valia-qa.docx')
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

#example with chroma
data = loader.load()

# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)

# Store 
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# Build prompt
template = """Eres un chatbot asistente amistoso y educado. 
    Utilizando la informacion proporcionada. Responde siempre de manera clara, directa, y muy concisa. 
    Cuando te pregunten sobre algo,retorna el enlace correspondiente que más ayudará a responder la pregunta. 
    Por ejemplo si te preguntan "¿Como subo una transacción?" 
    responde "Aquí puedes ver un tutorial sobre como subir una transacción" y comparte el enlace correspondiente
    {context}
    Pregunta: {question}
    Respuesta:"""

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# memory.save_context({"input": "Que es Valia?"}, {"output": "Valia es una empresa de Software y tecnología especialmente diseñada para Agentes Inmobiliarios. Fue fundada en el año 2018 en USA con el objetivo de desarrollar soluciones digitales para los agentes de todo el mundo y en especial de Latinoamérica."})
# memory.save_context({"input": "Que se puede hacer con valia?"}, {"output": "on Valia puedes crear tu perfil como agente inmobiliario, publicar anuncios de propiedades ilimitados de forma gratuita, construir tu historial de transacciones, agregar reseñas de clientes satisfechos, y aprovechar los beneficios del Plan Profesional ValiaPro. También puedes utilizar el News Feed para estar actualizado con las novedades del mercado inmobiliario, participar en el programa Valia Flex y crear tus propias colecciones de propiedades."})

chain_kwargs = {
    "prompt": QA_CHAIN_PROMPT,
}
chat = ConversationalRetrievalChain.from_llm(llm, retriever=vectorstore.as_retriever(), memory=memory, combine_docs_chain_kwargs=chain_kwargs)

print(chat.memory)

result = chat({"question": question})

answer = result['answer']

print('result ---------------------------------------------------- ')
print(answer)

# print(response)