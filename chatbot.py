import string #to transform string

def preprocess(text): #cleaning the text
    text = text.lower() #turns any text to lower case
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def detect_intent(text): #defining the intent of message
    greetings = {"hi", "hello", "hey"}
    farewells = {"bye", "goodbye", "see", "you"}

    words = set(text.split()) #to identify each word separately

    if words & greetings:
        return "greetings"
    elif words & farewells:
        return "farewells"
    else:
        return "unknown"
    

def ai_chatbot(user_input): #function for chatbot
    clean_input = preprocess(user_input)
    intent = detect_intent(clean_input)

    print (clean_input)
    print (intent)

    if intent == "greetings":
        return "Hello"
    elif intent == "farewells":
        return "Goodbye"
    else:
        return "I dont understand"
    

while True:
    user = input("you:")
    print("bot:", ai_chatbot(user))


    
    


