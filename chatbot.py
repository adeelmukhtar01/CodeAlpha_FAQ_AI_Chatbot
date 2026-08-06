from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pandas as pd
from rapidfuzz import process

# -------------------------
# Load Excel Data
# -------------------------
# Excel columns expected: | Category | Question | Keywords | Answer |
try:
    faq_data = pd.read_excel(
        "faq_data.xlsx",
        engine="openpyxl"
    )
    # Convert text columns safely
    questions = faq_data["Question"].astype(str).tolist()
except Exception as e:
    print(f"Error loading Excel file: {e}")
    faq_data = pd.DataFrame(columns=["Category", "Question", "Keywords", "Answer"])
    questions = []

# -------------------------
# Theme Settings
# -------------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# -------------------------
# Application Window
# -------------------------
app = ctk.CTk()
app.title("🤖 FAQ AI Chatbot Pro")
app.geometry("1100x800")

# -------------------------
# Core Helper Functions
# -------------------------
def current_time():
    return datetime.now().strftime("%I:%M %p")

def save_chat(message):
    try:
        with open("chat_history.txt", "a", encoding="utf-8") as file:
            file.write(message + "\n")
    except Exception as e:
        print(f"Error writing to chat history: {e}")

def show_about():
    messagebox.showinfo(
        "About",
        "FAQ AI Chatbot Pro\n\n"
        "Version: 1.0\n\n"
        "Developed by Adeel Mukhtar\n"
        "BS Artificial Intelligence"
    )

def clear_chat():
    chat_box.configure(state="normal")
    chat_box.delete("1.0", "end")
    welcome_text = (
        "🤖 Welcome to FAQ AI Chatbot Pro!\n\n"
        "I can answer questions from the FAQ database.\n"
        "Type a question below, search a category (e.g., 'Python'), or click a suggested topic.\n\n"
    )
    chat_box.insert("end", welcome_text, "welcome")
    chat_box.configure(state="disabled")

def send_message():
    user_question = entry.get().strip()

    if not user_question:
        return

    status_label.configure(text="🟡 Status: Searching...")
    app.update()

    chat_box.configure(state="normal")

    # Display & Log User Input
    user_msg = f"👤 You [{current_time()}]:\n{user_question}\n\n"
    chat_box.insert("end", user_msg, "user")
    save_chat(user_msg)

    # 1. Check for Category Match (e.g. "Python", "AI", "ML")
    category_input = user_question.lower()
    if "Category" in faq_data.columns:
        matches = faq_data[faq_data["Category"].astype(str).str.lower() == category_input]
        
        if len(matches) > 0:
            cat_header = f"📚 {category_input.upper()} FAQs [{current_time()}]:\n"
            chat_box.insert("end", cat_header, "bot")
            save_chat(cat_header)

            cat_body = ""
            for _, row in matches.iterrows():
                item = f"• {row['Question']}\n"
                cat_body += item

            cat_body += "\n"
            chat_box.insert("end", cat_body, "bot")
            save_chat(cat_body)

            chat_box.see("end")
            chat_box.configure(state="disabled")
            status_label.configure(text="🟢 Status: Ready")
            entry.delete(0, "end")
            return

    # 2. Fuzzy Matching with Confidence Score
    match = process.extractOne(user_question, questions) if questions else None

    if match:
        matched_question = match[0]
        confidence = match[1]

        if confidence >= 60:
            answer = faq_data.loc[
                faq_data["Question"] == matched_question,
                "Answer"
            ].values[0]

            bot_msg = (
                f"🤖 Bot [{current_time()}]\n"
                f"Confidence: {confidence:.1f}%\n"
                f"{answer}\n\n"
            )
            chat_box.insert("end", bot_msg, "bot")
            save_chat(bot_msg)
        else:
            error_msg = (
                f"🤖 Bot [{current_time()}]\n"
                f"Confidence: {confidence:.1f}%\n"
                "Sorry, I couldn't find a suitable answer.\n\n"
            )
            chat_box.insert("end", error_msg, "error")
            save_chat(error_msg)
    else:
        error_msg = (
            f"🤖 Bot [{current_time()}]\n"
            "Sorry, no questions found in the database.\n\n"
        )
        chat_box.insert("end", error_msg, "error")
        save_chat(error_msg)

    chat_box.see("end")
    chat_box.configure(state="disabled")
    status_label.configure(text="🟢 Status: Ready")
    entry.delete(0, "end")

def ask_suggested(question_text):
    entry.delete(0, "end")
    entry.insert(0, question_text)
    send_message()

# -------------------------
# Menu Bar Setup
# -------------------------
menu_bar = tk.Menu(app)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Clear Chat", command=clear_chat)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Help Menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

app.config(menu=menu_bar)

# -------------------------
# Main Container Structure
# -------------------------
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True)

# Left Sidebar
sidebar = ctk.CTkFrame(main_frame, width=180, corner_radius=0)
sidebar.pack(side="left", fill="y")

# Right Content Region
content = ctk.CTkFrame(main_frame, corner_radius=0)
content.pack(side="right", fill="both", expand=True)

# -------------------------
# Sidebar Elements
# -------------------------
logo = ctk.CTkLabel(
    sidebar,
    text="🤖\nFAQ AI\nChatbot",
    font=("Segoe UI", 22, "bold"),
    justify="center"
)
logo.pack(pady=25)

def sidebar_button(text, command=None):
    btn = ctk.CTkButton(
        sidebar,
        text=text,
        width=150,
        height=45,
        corner_radius=10,
        command=command
    )
    btn.pack(pady=8)
    return btn

sidebar_button("🏠 Home")
sidebar_button("📘 FAQs")
sidebar_button("📝 History")
sidebar_button("🗑 Clear Chat", clear_chat)
sidebar_button("ℹ️ About", show_about)
sidebar_button("❌ Exit", app.quit)

# -------------------------
# Content Region Elements
# -------------------------
title = ctk.CTkLabel(
    content,
    text="🤖 FAQ AI Chatbot Pro",
    font=("Segoe UI", 26, "bold")
)
title.pack(pady=(15, 2))

subtitle = ctk.CTkLabel(
    content,
    text="Your Intelligent FAQ Assistant",
    font=("Segoe UI", 14),
    text_color="gray"
)
subtitle.pack(pady=(0, 5))

# Chat Box Area (Auto-Resizing & Scrollable)
chat_box = ctk.CTkTextbox(
    content,
    font=("Segoe UI", 14)
)
chat_box.pack(fill="both", expand=True, padx=20, pady=10)

# Tag configurations for text colors
chat_box.tag_config("user", foreground="#4FC3F7")
chat_box.tag_config("bot", foreground="#7CFC00")
chat_box.tag_config("error", foreground="#FF6B6B")
chat_box.tag_config("welcome", foreground="#FFD700")

# Initial welcome message
chat_box.configure(state="normal")
chat_box.insert(
    "end",
    "🤖 Welcome to FAQ AI Chatbot Pro!\n\n"
    "I can answer questions from the FAQ database.\n"
    "Type a question below, search a category (e.g., 'Python'), or click a suggested topic.\n\n",
    "welcome"
)
chat_box.configure(state="disabled")

# Suggested Questions Cards
suggested_label = ctk.CTkLabel(
    content,
    text="💡 Suggested Questions",
    font=("Segoe UI", 16, "bold")
)
suggested_label.pack(pady=(5, 2))

cards_frame = ctk.CTkFrame(content, fg_color="transparent")
cards_frame.pack(pady=5)

questions_cards = [
    "🤖 What is Artificial Intelligence?",
    "📘 What is Machine Learning?",
    "🐍 What is Python?",
    "💬 What is ChatGPT?",
    "🧠 What is Deep Learning?",
    "📊 What is Data Science?"
]

for i, text in enumerate(questions_cards):
    real_question = text.split(" ", 1)[1]

    card = ctk.CTkButton(
        cards_frame,
        text=text,
        width=260,
        height=48,
        corner_radius=12,
        font=("Segoe UI", 13),
        fg_color="#2B2B2B",
        hover_color="#3B82F6",
        command=lambda q=real_question: ask_suggested(q)
    )

    card.grid(
        row=i // 2,
        column=i % 2,
        padx=8,
        pady=5
    )

# Input Frame (Bottom Action Bar)
input_frame = ctk.CTkFrame(content, corner_radius=15)
input_frame.pack(fill="x", padx=20, pady=10)

entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="💬 Ask your question here...",
    height=45,
    font=("Segoe UI", 15)
)
entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
entry.bind("<Return>", lambda event: send_message())

send_btn = ctk.CTkButton(
    input_frame,
    text="📤 Send",
    width=110,
    height=42,
    corner_radius=12,
    font=("Segoe UI", 14, "bold"),
    command=send_message
)
send_btn.pack(side="left", padx=5, pady=10)

clear_btn = ctk.CTkButton(
    input_frame,
    text="🗑 Clear",
    width=110,
    height=42,
    fg_color="#C0392B",
    hover_color="#922B21",
    corner_radius=12,
    font=("Segoe UI", 14, "bold"),
    command=clear_chat
)
clear_btn.pack(side="left", padx=(5, 10), pady=10)

# Status Bar
status_label = ctk.CTkLabel(
    content,
    text="🟢 Status: Ready",
    anchor="w",
    font=("Segoe UI", 12)
)
status_label.pack(fill="x", padx=20, pady=(0, 10))

# -------------------------
# Run Loop
# -------------------------
app.mainloop()