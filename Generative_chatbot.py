
import requests
import json



def chat_ollama(prompt, context=''):
    response = requests.post('http://localhost:11434/api/generate', #Sends a request to Ollama's API 
                             json={
                                 "model": "llama3.2",
                                 "prompt":f"{context}\nUser:{prompt}\nAssistant:",
                                 "stream":False,
                             })
    return json.loads(response.text)['response']
system_context ="""You are a helpful, harmless, and honest AI assistant similar to Claude.

Your response style:
- Be genuinely helpful and go into appropriate depth
- Use clear structure (but don't overuse bullet points unless needed)
- Explain concepts thoroughly but concisely
- Provide practical examples and code when relevant
- Be conversational and natural, not robotic
- Anticipate follow-up questions
- Use emojis sparingly (only when it adds value)
- Break down complex topics into digestible pieces
- Offer multiple solutions when appropriate
- Be honest about limitations and uncertainties"""


while True:
    user_input = input().lower()
    
    if user_input.lower() in ['exit', 'bye','quit']:
        print("goodbye!")
        break
    response = chat_ollama(user_input, system_context)
    print(f"\n{response}\n")
