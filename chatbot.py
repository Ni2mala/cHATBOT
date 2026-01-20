import string #to transform string
chat_memory=[] #to store chat history


INTENTS = {
    "greetings":{
        "keywords": {"hi", "hello", "hey"},
        "response": "Hello"
    },
    "farewells":{
        "keywords": {"bye", "goodbye", "see"},
        "response": "Goodbye"
    },
    "status":{
        "phrases": {"how are you", "how r you"},
        "response": "I am fine, thank you! How about you?"
    }
}

def preprocess(text): #cleaning the text
    text = text.lower() #turns any text to lower case
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def detect_intent(text): #defining the intent of message
    for intent, data in INTENTS.items():
        if "phrases" in data:
            for phrase in data["phrases"]:
                if phrase in text:
                    return intent
                
    words = set(text.split()) #to identify each word separately

    for intent, data in INTENTS.items():
        if "keywords" in data and words & data["keywords"]:
            return intent
        
    return "unknown"
    

def ai_chatbot(user_input): #function for chatbot
    clean_input = preprocess(user_input)
    intent = detect_intent(clean_input)

    chat_memory.append({
        "user": user_input,
        "intent": intent
    })

    return INTENTS.get(intent, {}).get("response", "I dont understand")
    
while True:
    user = input("you:")
    print("bot:", ai_chatbot(user))


    
    


