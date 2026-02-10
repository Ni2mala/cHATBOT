
import requests
import json
 
conversation_history = []
system_context ="""You are a professional customer support assistant 
for an online clothing brand. Help customers with:
- Product details (size, color, fabric, fit, care)
- Pricing, discounts, availability
- Orders, shipping, tracking
- Returns, exchanges, refunds
Be clear, friendly, and concise."""
def chat_ollama(message_list):
    response = requests.post('http://localhost:11434/api/chat', #Sends a request to Ollama's API 
                             json={
                                 "model": "llama3.2",
                                 "messages":message_list,
                                 "stream":False,
                             })
    return response.json()['message']['content']


#save chat memory 
def save_chat(history_to_save,filename="chat_history.json"):
    with open(filename, "w") as f:
        data ={"chat_history": history_to_save}
        json.dump(data, f, indent=2)
        return True

#imagine you are talking to someone with 10 second amnesia,
#you need to remind them every last 10 seconds of conversation 

def chat_with_memory(user_input, conversation_history, system_context):
    while len(conversation_history) > 20:

        del conversation_history[0:2]# Limit history to last 20 messages
    message_list = [{"role": "system", "content": system_context}]
    message_list.extend(conversation_history)
    message_list.append({"role": "user", "content": user_input})

    print("----Sending to Ollama API----")
    print(json.dumps(message_list, indent =2))

    response = chat_ollama(message_list)
    """full_context = system_context
    for msg in conversation_history:
        full_context += f"\n{msg}"#glues every old question and answer onto the new question, so the model can remember the conversation history

    response = chat_ollama(user_input, full_context)"""

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": response})

    return response



while True:
    user_input = input().lower()
    
    if user_input.lower() in ['exit', 'bye','quit']:
        save_chat(conversation_history)
        print("goodbye!")
        break
    response = chat_with_memory(user_input, conversation_history, system_context)
    print(f"\n{response}\n")




