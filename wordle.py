"""
Wordle!
"""

import argparse
from random import choice
from typing import Iterable
from urllib.request import urlopen

from colorama import init, Style, Back


class Wordle:
    def __init__(self, wordlist: Iterable[str]):
        self.wordlist = set(wordlist)

    def input_error(self, guess: str) -> str:
        """
        Check whether guess is valid.
        :returns None if the guess is valid, or an error message if it is invalid
        """
        if len(guess) != 5:
            return "Please enter a 5-letter word"
        if guess not in self.wordlist:
            return "Unknown word, try again"

    def random_word(self) -> str:
        return choice(list(self.wordlist))

    def validate_guess(self, guess: str) -> str:
        if len(guess) != 5:
            print("Please enter a 5-letter word")
        elif guess not in self.wordlist:
            print("Unknown word, try again")


def wordle_from_url(url: str) -> Wordle:
    words = (line.decode("utf-8").strip()
             for line in urlopen(url))
    return Wordle(words)


def color_code_char(character: str, correct: bool, in_word: bool) -> str:
    if correct:
        pre = Back.GREEN
    elif in_word:
        pre = Back.YELLOW
    else:
        pre = ""
    return f"{pre}{character}{Style.RESET_ALL}"


def color_code(guess: str, word: str):
    output = []
    for i, char in enumerate(guess):
        correct = char == word[i]
        in_word = char in word
        output.append(color_code_char(char, correct=correct, in_word=in_word))
    return "".join(output)


def play_wordle(wordle: Wordle, word: str):
    # Initialize colorama
    init()
    print("Let's play wordle!")
    for attempt in range(1, 7):
        print(f"Enter your next guess:")
        while True:
            guess = input(f"[{attempt}] ")
            error = wordle.validate_guess(guess)
            if error:
                print(error)
            else:
                break

        print(color_code(guess, word))
        if word == guess:
            print(f"Congrats! You needed {attempt} attempts")
            break
    else:
        print(f"Bad luck! We were looking for {word}")


WORD_LISTS = {
    "en": "https://raw.githubusercontent.com/jason-chao/wordle-solver/main/english_words_original_wordle.txt"
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    languages = list(WORD_LISTS.keys())
    parser.add_argument("--language", choices=WORD_LISTS.keys(), default=languages[0])
    parser.add_argument("--spoiler", action="store_true")
    args = parser.parse_args()
    url = WORD_LISTS[args.language]
    wordle = wordle_from_url(url)
    word = wordle.random_word()
    if args.spoiler:
        print(f"Correct word (for testing): {word}")
    play_wordle(wordle, word)
