from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "FAQs"

# Headers
ws.append(["Question", "Answer"])

# Data
ws.append([
    "What is Artificial Intelligence?",
    "Artificial Intelligence (AI) is the simulation of human intelligence by machines."
])

ws.append([
    "What is Machine Learning?",
    "Machine Learning is a branch of AI that enables computers to learn from data."
])

ws.append([
    "What is Python?",
    "Python is a high-level programming language widely used for AI, web development, and automation."
])

ws.append([
    "What is ChatGPT?",
    "ChatGPT is an AI chatbot developed by OpenAI."
])

ws.append([
    "What is Deep Learning?",
    "Deep Learning is a subset of Machine Learning that uses neural networks with multiple layers."
])

ws.append([
    "What is Data Science?",
    "Data Science is the process of collecting, analyzing, and interpreting data to gain useful insights."
])

wb.save("faq_data.xlsx")

print("✅ faq_data.xlsx created successfully!")