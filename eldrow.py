from colorama import init, Style, Back
from urllib.request import urlopen
from random import choice
COLORS = {"CORRECT": Back.GREEN, "INWORD": Back.YELLOW, "INCORRECT": ""}

class eldrow_game(object):
    def __init__(self, word, words, attempts):
        self.word = word
        self.words = words
        self.attempts = attempts

    def guesser(self, attempt):
        # Input a guess for the word
        print(f"Enter your next guess:")
        self.guess = input(f" {attempt} ")

    def evaluate_character(self, index):
        #evaluating whether character in guessword is correct
        if self.guess[index] == self.word[index]:
            return "CORRECT"
        if self.guess[index] in self.word:
            return "INWORD"
        return "INCORRECT"

    def color_code_character(self, character, evaluation):
        # color code whether guessword characters are correct
        color = COLORS[evaluation]
        return f"{color}{character}{Style.RESET_ALL}"

    def score_guess(self):
        # Use the character scores to score the guessword
        output = []
        if len(self.guess) != 5:
            print("Please add a 5-letter word")
            self.attempts += 1
        elif self.guess.encode("utf-8") not in self.words:
            print("Unknown word, try again")
            self.attempts += 1
        else:
            for i in range(len(self.guess)):
                evaluation = self.evaluate_character(i)
                coded_char = self.color_code_character(self.guess[i], evaluation)
                output.append(coded_char)
            score = "".join(output)
            print(score)


    def play_game(self):
        # Initate the game with the setting specified before (attempts, word, and wordlist specified
        print("Let's play wordle!")
        print("Enter a guess")
        #print(f"Correct word (for testing): {self.word}")

        for attempt in range(self.attempts):
            self.guesser(attempt)
            self.score_guess()

            if self.word == self.guess:
                print(f"Congrats! You needed {attempt} attempts")
                break
        if self.word != self.guess:
            print(f"Bad luck! We were looking for {word}")

def define_word(url):
    words = []
    for line in urlopen(url):
        words.append(line.strip())
    word = choice(words).decode("utf-8")
    return word, words

# define the word and words to be used
url = "https://raw.githubusercontent.com/jason-chao/wordle-solver/main/english_words_original_wordle.txt"
word, words = define_word(url)

#specify game setting (word to guess, wordlist, and attempts)
game_setup = eldrow_game(word, words, attempts=5)

# Initate the game with the setting specified before (attempts, word, and wordlist specified
game_setup.play_game()