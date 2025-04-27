import tkinter as tk
import random

words = [
    "apple", "banana", "grape", "cherry", "orange",
    "mango", "plum", "apricot", "grapefruit", "avocado",
    "guava", "sapodilla", "lychee", "watermelon",
    "pomegranate", "pear", "cherry", "strawberry", "melon", "damson",
    "papaya", "coconut", "peach", "shaddock", "gooseberry", "durian",
    "raspberry", "kiwi", "jackfruit", "jamun", "mulberry", "persimmon",
    "quince", "jujube", "elderberry", "olive", "tamarind", "sugarcane",
    "dates", "fig", "blueberry", "carambola", "cranberry", "pineapple"
]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruity Hangman Game")

        self.word = random.choice(words)
        self.guessed = []
        self.wrong_guesses = 0

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.label_title = tk.Label(root, text="Fruity Hangman Game 🎯", font=("Comic Sans MS", 20))
        self.label_title.pack()

        self.draw_base()

        self.label = tk.Label(root, text=self.get_display_word(), font=("Comic Sans MS", 24))
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Guess", command=self.make_guess)
        self.button.pack()

        self.reset_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.reset_button.pack()

    def draw_base(self):
        self.canvas.create_line(50, 350, 150, 350)  # Base
        self.canvas.create_line(100, 350, 100, 50)  # Pole
        self.canvas.create_line(100, 50, 250, 50)   # Top beam
        self.canvas.create_line(250, 50, 250, 100)  # Rope

    def get_display_word(self):
        return " ".join([char if char in self.guessed else "_" for char in self.word])

    def make_guess(self):
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if letter in self.word:
            self.guessed.append(letter)
        else:
            self.wrong_guesses += 1
            self.draw_hangman()

        self.label.config(text=self.get_display_word())

        if "_" not in self.get_display_word():
            self.label.config(text=f"You won! 🎉 The word was '{self.word}'")

        if self.wrong_guesses >= 6:
            self.label.config(text=f"You lost! 😢 The word was '{self.word}'")

    def draw_hangman(self):
        if self.wrong_guesses == 1:
            self.canvas.create_oval(225, 100, 275, 150)  # Head
        elif self.wrong_guesses == 2:
            self.canvas.create_line(250, 150, 250, 250)  # Body
        elif self.wrong_guesses == 3:
            self.canvas.create_line(250, 170, 220, 200)  # Left arm
        elif self.wrong_guesses == 4:
            self.canvas.create_line(250, 170, 280, 200)  # Right arm
        elif self.wrong_guesses == 5:
            self.canvas.create_line(250, 250, 220, 300)  # Left leg
        elif self.wrong_guesses == 6:
            self.canvas.create_line(250, 250, 280, 300)  # Right leg

    def restart_game(self):
        self.word = random.choice(words)
        self.guessed = []
        self.wrong_guesses = 0
        self.canvas.delete("all")
        self.draw_base()
        self.label.config(text=self.get_display_word())

root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
