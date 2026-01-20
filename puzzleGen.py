#!usr/bin/python3

import pandas as pd
from dataclasses import dataclass


@dataclass
class CWord:
    word: str
    start: {int, int}
    vertical: bool
    question: str


def get_puzzle_piece(file, word_num):
    df_it = pd.read_csv(file, encoding="ISO-8859-1", chunksize=word_num)
    for chunk in enumerate(df_it):
        return chunk


def print_puzzle(answers, qs) -> int:
    crossword = list[CWord]
    word_count = 0
    for word in answers:
        coords = can_it_fit(word, crossword)
        ok = insert_into_crossword(word, crossword, coords)
        if ok:
            word_count += 1
    return word_count


def can_it_fit(word, crossword):
    for c in word:
        for cword in crossword:
            for char in cword.word:
                if c == char:
                    return cword.word


def insert_into_crossword(word, crossword) -> bool:
    return True


file = f"nytcrosswords.csv"
piece = get_puzzle_piece(file, 5)
print(piece)


crossword = []
crossword.append(
    CWord(
        word="PAT",
        start={0, 0},
        vertical=False,
        question="Action done while saying good dog",
    )
)
crossword.append(CWord(word="SEP", start={0, 0}, vertical=True, question="Fall mo"))
print(can_it_fit("wArd", crossword))
