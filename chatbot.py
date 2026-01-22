import string #to transform string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

chat_memory=[] #to store chat history


training_data = [
    ("hi", "greetings"),
    ("hello", "greetings"),
    ("hey there", "greetings"),
    ("bye", "farewells"),
    ("goodbye", "farewells"),
    ("how are you", "status"),
    ("how are things", "status"),
    ("how is it going", "status"),
]

INTENT_RESPONSES = {
    "greetings": "Hello",
    "farewells": "Goodbye",
    "status": "I am fine, thank you! How about you?"
}


texts= [t[0] for t in training_data]
labels = [t[1] for t in training_data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)


def preprocess(text): #cleaning the text
    text = text.lower() #turns any text to lower case
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

#prediction with confidence threshold
def detect_intent(text): #predecting the intent
    X_test = vectorizer.transform([text])
    probs = model.predict_proba(X_test)[0]
    max_prob = max(probs)
    if max_prob < 0.4:
        return "unknown"
    return model.classes_[probs.argmax()]
   
                
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


    
    


