
def chatbot(data):

    chat_response = conversation.run(data['input'])

    print(history.messages)
    
    response = {
        'request': data,
        'response': chat_response,
    }

    return response