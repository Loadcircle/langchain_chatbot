from flask import Flask, request, jsonify
from langchain import OpenAI, ConversationChain
from langchain.memory import ChatMessageHistory
from chatbot import chatbot

app = Flask(__name__)

class Config:
    OPENAI_KEY = ''
    # Otras configuraciones de la aplicación

app.config.from_object(Config)


@app.route("/")
def home():
    
    print(list)

    return "<p>Welcome to the chat gpt simple api</p>"


llm = OpenAI(temperature=0.9)
conversation = ConversationChain(llm=llm, verbose=True)
history = ChatMessageHistory()

@app.route("/input", methods=['POST'])
def input_message():
    data = request.get_json()

    chat_response = conversation.run(data['input'])

    print(history.messages)
    
    response = {
        'request': data,
        'response': chat_response,
    }

    return jsonify(response)
  