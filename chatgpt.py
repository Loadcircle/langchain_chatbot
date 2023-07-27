import os
import sys
import constants
import prompt
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import Docx2txtLoader
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


#production code -------------------------------------------------------
        
loader = Docx2txtLoader('data/Valia-qa.docx')
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
data = loader.load()

# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)
embedding=OpenAIEmbeddings()

# Store 
# rds = Redis.from_documents(documents=all_splits, embedding=embedding, redis_url="redis://localhost:6379", index_name="link")

# Load from existing index
rds = Redis.from_existing_index(embedding=embedding, redis_url="redis://localhost:6379", index_name="link")

# results = rds.similarity_search(question)
# print(results[0].page_content)

# sys.exit(1) 
# vectorstore = Chroma.from_documents(documents=all_splits, )

# Build prompt
template = prompt.template

QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

#set previous memory history
for input, output in memoryHistory:
    memory.save_context({"input": input}, {"output": output})

chain_kwargs = {
    "prompt": QA_CHAIN_PROMPT,
}
chat = ConversationalRetrievalChain.from_llm(llm, retriever=rds.as_retriever(), memory=memory, combine_docs_chain_kwargs=chain_kwargs)

result = chat({"question": question})

answer = result['answer']

memoryHistory.append((question, answer))
guardar_memory_history()

print('----------------------------------------------------')
print(answer)