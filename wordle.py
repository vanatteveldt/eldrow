"""
Wordle!
"""

import argparse
from random import choice
from typing import Iterable, Union
from urllib.request import urlopen

from colorama import init, Style, Back


class Wordle:
    def __init__(self, wordlist: Iterable[str]) -> None:
        """
        Creates a Wordle object from a list of possible 5-letter words.
        :param wordlist: list of possible words to play Wordle with.
        """
        self.wordlist = set(wordlist)

    def random_word(self) -> str:
        """
        Retrieve random word from the downloaded list of words.
        :return: string of random chosen word.
        """
        return choice(list(self.wordlist))

    def validate_guess(self, guess: str) -> Union[str, None]:
        """
        Check whether guess is valid.
        :param guess: string with the candidate word from the user input.
        :return: None if the guess is valid, or an error message if it is invalid.
        """
        if len(guess) != 5:
            return "Please enter a 5-letter word"
        elif guess not in self.wordlist:
            return "Unknown word, try again"
        return None

    def get_guess(self, prompt: str = ">") -> str:
        """
        Get a valid guess from the user
        :param prompt: The prompt to show the user
        :return: a valid 5 letter word
        """
        while True:
            guess = input(prompt)
            error = self.validate_guess(guess)
            if error:
                print(error)
            else:
                return guess


def wordle_from_url(url: str) -> Wordle:
    """
    Downloads list of words from the given URL and creates a Wordle object from it.
    :param url: URL to retrieve the list of words.
    :return: Wordle object to play the game.
    """
    words = (line.decode("utf-8").strip()
             for line in urlopen(url))
    return Wordle(words)


def color_code_char(character: str, correct: bool, in_word: bool) -> str:
    """
    Changes color of the character, depending on if it has been guessed correctly or not.
    :param character: string indicating the character.
    :param correct: flag indicating if the character guessed is at the correct place.
    :param in_word: flag indicating if the character is present in the word.
    :return: returns the character with its correct color.
    """
    if correct:
        pre = Back.GREEN
    elif in_word:
        pre = Back.YELLOW
    else:
        pre = ""
    return f"{pre}{character}{Style.RESET_ALL}"


def color_code(guess: str, word: str) -> str:
    """
    Gets the correct coloring for the entire word, depending on how well it is guessed by the user.
    :param guess: string containing the guessed word by the user.
    :param word: string containing the original word that has to be guessed.
    :return: string that outputs the guessed word with the correct colors.
    """
    output = []
    for i, char in enumerate(guess):
        correct = char == word[i]
        in_word = char in word
        output.append(color_code_char(char, correct=correct, in_word=in_word))
    return "".join(output)


def play_wordle(wordle: Wordle, word: str) -> None:
    """
    Function to play the Wordle game from the beginning to end.
    :param wordle: Wordle object that takes care of choosing the word and checking the guesses.
    :param word: word that has to be guessed.
    :return: None
    """
    # Initialize colorama
    init()
    print("Let's play wordle!")
    for attempt in range(1, 7):
        guess = wordle.get_guess(f"[{attempt}] ")
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

    if args.language not in WORD_LISTS:
        print("Only English words available.")

    url = WORD_LISTS[args.language]
    wordle = wordle_from_url(url)
    word = wordle.random_word()
    if args.spoiler:
        print(f"Correct word (for testing): {word}")
    play_wordle(wordle, word)
