import string #to transform string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import random
import re
import json #for saving and loading data in json format
from datetime import datetime 

DEBUG_MODE = True #set to false to turn off debug message
chat_memory=[] #to store chat history
user_name = None #New store the user's name globally

training_data = [
    # Greetings - Different ways people say hello
    ("hi", "greetings"),
    ("hello", "greetings"),
    ("hey there", "greetings"),
    ("hey", "greetings"),
    ("good morning", "greetings"),
    ("good evening", "greetings"),
    ("good afternoon", "greetings"),
    ("what's up", "greetings"),
    ("howdy", "greetings"),
    ("hi there", "greetings"),
    
    # Farewells - Different ways to say goodbye
    ("bye", "farewells"),
    ("goodbye", "farewells"),
    ("see you later", "farewells"),
    ("see you", "farewells"),
    ("take care", "farewells"),
    ("catch you later", "farewells"),
    ("gotta go", "farewells"),
    ("talk to you later", "farewells"),
    
    # Status - Asking how the bot is doing
    ("how are you", "status"),
    ("how are things", "status"),
    ("how is it going", "status"),
    ("how are you doing", "status"),
    ("what's going on", "status"),
    ("how's everything", "status"),
    
    # Thanks - When user says thank you
    ("thank you", "thanks"),
    ("thanks", "thanks"),
    ("thanks a lot", "thanks"),
    ("appreciate it", "thanks"),
    ("thank you so much", "thanks"),
    ("cheers", "thanks"),
    
    # Help - When user needs assistance
    ("help me", "help"),
    ("i need help", "help"),
    ("can you help", "help"),
    ("assist me", "help"),
    ("i need assistance", "help"),
    ("help", "help"),
    
    # Bot name - When user asks about the bot
    ("what is your name", "bot_name"),
    ("who are you", "bot_name"),
    ("your name", "bot_name"),
    ("tell me your name", "bot_name"),
    ("what should i call you", "bot_name"),

     # Introduction - NEW INTENT
    ("my name is john", "introduction"),
    ("i am sarah", "introduction"),
    ("call me mike", "introduction"),
    ("i'm alex", "introduction"),
    ("this is tom", "introduction"),
    ("my name is alice", "introduction"),
    ("you can call me bob", "introduction"),
    
    # Jokes - When user wants to laugh
    ("tell me a joke", "joke"),
    ("make me laugh", "joke"),
    ("say something funny", "joke"),
    ("do you know any jokes", "joke"),
    ("joke please", "joke"),
    ("i need a joke", "joke"),
    
    # Time - When user asks about time
    ("what time is it", "time"),
    ("tell me the time", "time"),
    ("what's the time", "time"),
    ("current time", "time"),
    ("time please", "time"),
    
    # Date - When user asks about date
    ("what's the date", "date"),
    ("what is today's date", "date"),
    ("tell me the date", "date"),
    ("what day is it", "date"),
    ("today's date", "date"),
    
    # Capabilities - When user asks what bot can do
    ("what can you do", "capabilities"),
    ("what are your capabilities", "capabilities"),
    ("help me understand what you can do", "capabilities"),
    ("what features do you have", "capabilities"),
    ("tell me about yourself", "capabilities"),
    
    # Small talk - Compliments
    ("you are great", "compliment"),
    ("you are awesome", "compliment"),
    ("you're amazing", "compliment"),
    ("good job", "compliment"),
    ("well done", "compliment"),
    ("you're smart", "compliment"),
    
    # Small talk - How old
    ("how old are you", "age"),
    ("what is your age", "age"),
    ("when were you born", "age"),
    ("your age", "age"),

]

INTENT_RESPONSES = {
    "greetings": [
        "Hello! How can I help you today?",
        "Hi there! What can I do for you?",
        "Hey! How's it going?",
        "Hello! Nice to meet you!"
    ],
    "farewells": [
        "Goodbye! Have a great day!",
        "See you later!",
        "Take care! Come back anytime!",
        "Bye! It was nice talking to you!"
    ],
    "status": [
        "I'm doing great, thank you! How about you?",
        "I'm fine! How can I assist you today?",
        "I'm here and ready to help! How are you?",
        "Doing well! What brings you here today?"
    ],
    "thanks": [
        "You're welcome!",
        "Happy to help!",
        "Anytime!",
        "Glad I could assist!",
        "No problem at all!"
    ],
    "help": [
        "Sure! What do you need help with?",
        "I'm here to assist. What's the issue?",
        "Of course! Tell me what you need.",
        "I'd be happy to help! What's up?"
    ],
    "bot_name": [
        "I'm your AI assistant!",
        "You can call me ChatBot!",
        "I'm an AI chatbot here to help you!",
        "My name is ChatBot, nice to meet you!"
    ],
    "unknown": [
        "I'm not sure I understand. Could you rephrase that?",
        "I didn't quite get that. Can you try again?",
        "Hmm, I'm not familiar with that. Can you explain differently?",
        "Sorry, I don't understand. Could you say that another way?"
    ],
    "introduction": [
        "Nice to meet you, {name}!",
        "Hello {name}! Great to meet you!",
        "Hi {name}! How can I help you today?",
        "Welcome {name}! What can I do for you?"
    ],
    "joke":[
        "{joke}",
    ],
    "time":[
        "The current time is {time}.",
        "It's {time} right now.",
        "Right now it's {time}.",
    ],
    "date": [
        "Today's date is {date}.",
        "It's {date} today.",
        "Today is {date}.",
    ],
    "capabilities": [
        "I can help you with several things:\n• Have conversations and remember your name\n• Tell you the time and date\n• Tell jokes\n• Answer basic questions\n• And more! Just ask me anything!",
        "I'm here to assist! I can:\n• Chat with you\n• Remember your name\n• Tell jokes and the time/date\n• Keep track of our conversation history\nWhat would you like to do?",
    ],
    "compliment": [
        "Thank you! You're very kind!",
        "Aww, thanks! You made my day!",
        "That's so nice of you to say!",
        "Thank you! I'm just trying my best to help!",
        "You're awesome too! Thanks for the compliment!",
    ],
    "age": [
        "I'm an AI, so I don't really have an age!",
        "I was created recently, but I don't age like humans do!",
        "Age is just a number for humans, but I'm timeless! 😊",
        "I'm as old as this conversation, and as young as the next one!",
    ],


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

def extract_entities(text): #function to extract entities
    """
Extracts useful information from user input like names.
args: 
    text: the user's message
returns:
    dictionary containing found entities
    """
    entities = {}
    name_pattern = [
        r"my name is (\w+)",
        r"i am (\w+)",
        r"i'm (\w+)",
        r"call me(\w+)",
        r"this is(\w+)"
    ]

    #check each pattern
    text_lower = text.lower()
    for pattern in name_pattern:
        match = re.search(pattern, text_lower)
        if match:
            #capitalize the first letter of the name
            entities['name'] = match.group(1).capitalize()
            break
    return entities

def save_chat_history(filename = "chat_history.json"):

    """
Saves chat memory to jason file
Args:
    filename :Name of the file to save to (dfault:chathistory.json)
    """
    try:
        with open (filename, 'w') as f:
            data={
                "user_name": user_name,
                "chat_history": chat_memory
            }
            json.dump(data, f, indent=2)
        if DEBUG_MODE:
            print(f"[DEBUG] chat history saved to {filename}")
        return True
    except Exception as e:
        print(f"[ERROR] Could not save chat hsitory:{e}")
        return False
    

def load_chat_history(filename = "chat_history.json"):
    """
loads chat history from json file.
args:
    filename: Nmae of the file to load from (default: chat_history.json)
Returns:
    True if loaded successfully, Flase otherwise
     """
    global chat_memory, user_name
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            chat_memory = data.get("chat_history",[])
            user_name = data.get("user_name", None)
        
        if DEBUG_MODE:
            print(f"[DEBUG] loaded {len(chat_memory)} messages from history")
            if user_name:
                print(f"[DEBUG] Remembered username: {user_name}")

        return False
    
    except Exception as e:
        print(f"[ERROR] could not load the chat history: {e}")
        return False
    
def get_current_time():
    """
    Returns the current time in a readable format
    """
    now = datetime.now()
    return now.strftime("%I:%M%p")

def get_current_date():
    now = datetime.now()
    return now.strftime("%B %d %Y")

def get_random_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "What do you call a bear with no teeth? A gummy bear!",
        "Why don't eggs tell jokes? They'd crack each other up!",
        "What did the ocean say to the beach? Nothing, it just waved!",
        "Why did the math book look sad? Because it had too many problems!",
        "What do you call a fake noodle? An impasta!",
        "Why can't a bicycle stand on its own? It's two tired!",
    ]
    return random.choice(jokes)


def view_chat_history():
    """
    displays the chat history in readbale format"""
    if not chat_memory:
        print("\n [No chat history yet]\n")
        return
    print("Chat History")

    for i, entry in enumerate(chat_memory, 1):
        print(f"\n[{i}] You: {entry['user']}")
        print(f"\n Intent: {entry['intent']}")
        if entry.get('entities'):
            print(f" Entities:{entry['entities']}")



#prediction with confidence threshold
def detect_intent(text): #predecting the intent
    X_test = vectorizer.transform([text])
    probs = model.predict_proba(X_test)[0]
    max_prob = max(probs)
    if DEBUG_MODE:
        predicted = model.classes_[probs.argmax()]
        print(f"[DEBUG] Predicted intent: {predicted} with probability {max_prob:.2f}")
    if max_prob < 0.2:
        return "unknown"
    return model.classes_[probs.argmax()]
   
                
def ai_chatbot(user_input): #function for chatbot
    global user_name
    clean_input = preprocess(user_input)
    entities = extract_entities(user_input)
    intent = detect_intent(clean_input)
    if 'name' in entities:
        user_name = entities['name']
        if DEBUG_MODE:
            print(f"[DEBUG] learned user's name:, {user_name}")
    

    chat_memory.append({
        "user": user_input,
        "intent": intent,
        "entities": entities,
    })
    #get responses for this intent (either list or use""unknown" responses)
    responses = INTENT_RESPONSES.get(intent, INTENT_RESPONSES["unknown"])
    response = random.choice(responses)
    if user_name:
        # Special handling for introductions - replace {name} placeholder
        if intent == "introduction":
            response = response.replace("{name}", user_name)
        elif intent == 'greetings':
            response = f'Hello {user_name}! How can I help you today?'
        elif intent == "farewells":
            response= f'Goodbye {user_name}! Have a great day!'

    elif intent == "introduction":
            response = "Nice to meet you! What's your name?"

    #For dynamic response
    if intent =="joke":
        joke = get_random_joke()
        response = joke

    if intent =="time":
        current_time = get_current_time()
        response = response.replace("{time}", current_time)

    if intent =="date":
        current_date = get_current_date()
        response = response.replace("{date}", current_date)

    

    return response

    
        
load_chat_history()
if user_name:
    print(f"chatBot: Welcome back, {user_name}!")
else:
    print("CHatbot: Hello I'm your AI assistant.")
print("ChatBot: Type 'quit', 'exit', or 'bye' to end the conversation.") 

while True:
    user = input("you:").strip() #strip to remove extra spaces

    #checking if uer input is empty
    if not user:
        print("chatbot: Please enter a message.")
        continue #skip to next iteration if input is empty

    #check if user wants to view history
    if user.lower() == "history":
        view_chat_history()
        continue
    #check if user want to exit
    if user.lower() in ["bye", "exit", "quit"]:
        print("bot: Goodbye! Have a great day!")
        save_chat_history()
        break
    #get bot response
    print("bot:", ai_chatbot(user))
    if len(chat_memory)%5==0:
        save_chat_history()
    


    
    


