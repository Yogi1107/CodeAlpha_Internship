import random
import nltk
import webbrowser
import re
from nltk.chat.util import Chat, reflections
from datetime import datetime

# Define conversation patterns
pairs = [
    [
        r"(hi|hello|hey|holla|hola)",
        ["Hello! How can I help you today?", "Hi there! What can I do for you?"]
    ],
    [
        r"(.*)(your name)(.*)",
        ["I'm a chatbot created by you!", "I don't have a name yet. What would you like to call me?"]
    ],
    [
        r"(how are you|how's it going)",
        ["I'm doing well, thanks for asking! How about you?", "All good here! How can I assist you?"]
    ],
    [
        r"(.*)(help|support)(.*)",
        ["Sure, I'm here to help. Tell me what you need support with.", "Of course! What do you need help with?"]
    ],
    [
        r"(bye|goodbye|see you later)",
        ["Goodbye! Have a great day!", "See you soon! Stay awesome!"]
    ],
    [
        r"(.*)",
        ["I'm not sure I understand. Can you rephrase?", "Interesting... Tell me more!"]
    ]
]

# Initialize the chatbot
def main():
    print("Hi! I'm your friendly chatbot. Type 'quit' to exit.")
    chatbot = Chat(pairs, reflections)
    
    while True:
        user_input = input("> ")
        user_input = user_input.lower()
        
        if user_input == "quit":
            print("Goodbye! 👋")
            break
        
        # Handle specific commands based on user_input
        
        # If user types "hi" or "hello" etc., greet them
        if re.search(r"(hi|hello|hey|holla|hola)", user_input):
            print(random.choice(["Hello! How can I help you today?", "Hi there! What can I do for you?"]))
        
        # Handle opening YouTube
        elif "open youtube" in user_input:
            print("Opening YouTube for you!")
            webbrowser.open("https://www.youtube.com")
        
        # Search for a video on YouTube
        elif "search youtube" in user_input:
            search_query = user_input.replace("search youtube", "").strip()
            print(f"Searching YouTube for {search_query}...")
            webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")
        
        # Search on Google
        elif "search google" in user_input:
            search_query = user_input.replace("search google", "").strip()
            print(f"Searching Google for {search_query}...")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        
        # Read the news
        elif "news" in user_input or "show me the news" in user_input:
            print("Opening latest news...")
            webbrowser.open("https://news.google.com")
        
        # Handle weather request
        elif "weather" in user_input:
            print("Opening Weather Forecasts of India!")
            webbrowser.open("https://weather.com/en-IN/weather/today/l/INXX0096:1:IN")
        
        # Handle date request
        elif "date" in user_input:
            today = datetime.today().strftime('%d-%m-%Y')
            print(f"Today's date is: {today}")
        
        # If the command isn't recognized, use the chatbot's default responses
        else:
            print(chatbot.respond(user_input))

if __name__ == "__main__":
    main()
