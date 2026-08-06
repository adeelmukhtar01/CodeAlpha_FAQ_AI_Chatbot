from utils.faq_loader import FAQLoader
from utils.chatbot_logic import ChatbotLogic

loader = FAQLoader()
loader.load()

bot = ChatbotLogic(loader)

print("FAQ AI Chatbot Test")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = bot.get_response(question)

    if answer:
        print("Bot:", answer)
    else:
        print("Bot: Sorry, I couldn't find an answer.")