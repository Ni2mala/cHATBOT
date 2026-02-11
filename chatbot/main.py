# main.py

from chatbot import ChatBot

def main():
    bot = ChatBot()

    while True:
        user_input = input("> ").strip()

        if user_input.lower() in {"exit", "quit", "bye"}:
            bot.shutdown()
            print("Goodbye.")
            break

        response = bot.reply(user_input)
        print(response)
        print()

if __name__ == "__main__":
    main()
