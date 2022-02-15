import pytest
from colorama import Style, Back

from wordle import wordle_from_url, color_code

pre_correct = Back.GREEN
pre_somewhere = Back.YELLOW

WORD_LISTS = {
    "en": "https://raw.githubusercontent.com/jason-chao/wordle-solver/main/english_words_original_wordle.txt"
}
url = WORD_LISTS["en"]
wordle = wordle_from_url(url)


def test_picked_word():
    word = wordle.random_word()
    assert word
    assert len(word) == 5
    assert isinstance(word, str)


@pytest.mark.parametrize(
    "guess, word, colored",
    [
        ("later", "later", f"{pre_correct}l{Style.RESET_ALL}{pre_correct}a{Style.RESET_ALL}{pre_correct}t"
                           f"{Style.RESET_ALL}{pre_correct}e{Style.RESET_ALL}{pre_correct}r{Style.RESET_ALL}"),
        ("daily", "later", f"d{Style.RESET_ALL}{pre_correct}a{Style.RESET_ALL}i{Style.RESET_ALL}{pre_somewhere}l"
                           f"{Style.RESET_ALL}y{Style.RESET_ALL}"),
        ("niche", "boast", f"n{Style.RESET_ALL}i{Style.RESET_ALL}c{Style.RESET_ALL}h{Style.RESET_ALL}e"
                           f"{Style.RESET_ALL}"),
        ("traps", "stars", f"{pre_somewhere}t{Style.RESET_ALL}{pre_somewhere}r{Style.RESET_ALL}{pre_correct}a"
                           f"{Style.RESET_ALL}p{Style.RESET_ALL}{pre_correct}s{Style.RESET_ALL}")
    ],
)
def test_color_code(guess, word, colored):
    assert color_code(guess, word) == colored


@pytest.mark.parametrize(
    "n",
    [
        1, 5, 10
    ],
)
def test_random_word(n):
    words = [wordle.random_word() for _ in range(n)]
    assert len(words) == len(set(words))


@pytest.mark.parametrize(
    "guess, outcome",
    [
        ("later", None),
        ("stars", None),
        ("llall", "Unknown word, try again"),
        ("trrrr", "Unknown word, try again"),
        ("h", "Please enter a 5-letter word"),
        ("ha", "Please enter a 5-letter word"),
        ("hahahahaha", "Please enter a 5-letter word")
    ],
)
def test_validate_guess(guess, outcome):
    assert wordle.validate_guess(guess) == outcome
