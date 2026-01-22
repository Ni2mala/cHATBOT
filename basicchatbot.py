"""Ai chatbot assistant with if else condition"""


def ai_chatbot(user_input):
    user_input = user_input.lower()

    if user_input.lower() == "hi":
        return "hello"
    elif user_input.lower() == "bye":
        return "goodbye"
    elif user_input.lower() == "how are you?":
        return("I am good how are you")
    elif user_input.lower() == "k gardai xau":
        return "timilai sochdai xu"
    else:
        return "I don't understand"
    
    
while True:
    user = input("you :")
    response = ai_chatbot(user)
    print("bot :", response)

    if user.lower() == "bye":
        break