import string #to transform string
from collections import Counter 
import math
chat_memory=[] #to store chat history


INTENT_EXAMPLES = {
    "greetings": [
        "hi",
        "hello",
        "hey there"
    ],
    "farewells": [
        "bye",
        "goodbye",
        "see you"
    ],
    "status": [
        "how are you",
        "how are things",
        "how is it going"
    ]
}

INTENT_RESPONSES = {
    "greetings": "Hello",
    "farewells": "Goodbye",
    "status": "I am fine, thank you! How about you?"
}

def cosine_similarity(vect1, vect2):
    intersection = set(vect1.keys()) & set(vect2.keys())
    numerator = sum(vect1[x] * vect2[x] for x in intersection)
    sum1 = sum(v**2 for v in vect1.values())
    sum2 = sum(v**2 for v in vect2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return numerator / denominator

def text_to_vector(text):
    return Counter(text.split())

def preprocess(text): #cleaning the text
    text = text.lower() #turns any text to lower case
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def detect_intent(text): #defining the intent of message
    text_vec = text_to_vector(text)
    best_intent = None
    best_score = 0
    #loop through examples instead of phrase

    for intent, examples in INTENT_EXAMPLES.items():
        for example in examples:
            example_vec = text_to_vector(example)
            score = cosine_similarity(text_vec, example_vec)
            if score> best_score:
                best_score = score
                best_intent = intent    
    if best_score > 0.3:
        return best_intent
    return "unknown"
                
def ai_chatbot(user_input): #function for chatbot
    clean_input = preprocess(user_input)
    intent = detect_intent(clean_input)

    chat_memory.append({
        "user": user_input,
        "intent": intent
    })

    return INTENT_RESPONSES.get(intent, "I dont understand")
    
while True:
    user = input("you:")
    print("bot:", ai_chatbot(user))


    
    


