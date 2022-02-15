from colorama import init, Style, Back
from urllib.request import urlopen
from random import choice
init()
url = "https://raw.githubusercontent.com/jason-chao/wordle-solver/main/english_words_original_wordle.txt"
words = []
for line in urlopen(url):
    words.append(line.strip())
word = choice(words).decode("utf-8")
print("Let's play wordle!")
print(f"Correct word (for testing): {word}")
for attempt in [1,2,3,4,5,6]:
    print(f"Enter your next guess:")
    while True:
        guess = input(f"[{attempt}] ")
        if len(guess) != 5:
            print("Please enter a 5-letter word")
        elif guess.encode("utf-8") not in words:
            print("Unknown word, try again")
        else:
            break
    output = []
    if guess[0] == word[0]:
        output.append(Back.GREEN)
    elif guess[0] in word:
        output.append(Back.YELLOW)
    output.append(guess[0])

    output.append(Style.RESET_ALL)
    if guess[1] == word[1]:
        output.append(Back.GREEN)
    elif guess[1] in word:
        output.append(Back.YELLOW)
    output.append(guess[1])
    output.append(Style.RESET_ALL)
    if guess[2] == word[2]:
        output.append(Back.GREEN)
    elif guess[2] in word:
        output.append(Back.YELLOW)
    output.append(guess[2])
    output.append(Style.RESET_ALL)
    if guess[3] == word[3]:
        output.append(Back.GREEN)
    elif guess[3] in word:
        output.append(Back.YELLOW)
    output.append(guess[3])
    output.append(Style.RESET_ALL)
    if guess[4] == word[4]:
        output.append(Back.GREEN)
    elif guess[4] in word:
        output.append(Back.YELLOW)
    output.append(guess[4])
    output.append(Style.RESET_ALL)
    print("".join(output))
    if word == guess:
        print("Congrats! You needed {attempt} attempts")
        break
else:
    print(f"Bad luck! We were looking for {word}")
