#!usr/bin/python3

import pandas as pd
from dataclasses import dataclass


@dataclass
class CWord:
    word: str
    start: tuple[int, int]
    vertical: bool
    question: str


@dataclass
class puzzle:
    words: list[CWord]
    positions: list[
        list[str]
    ]  # (y, x) for everything! ALSO I figured this was easier than trying to have this be boolean, although that would make adding and removing words much more efficient.


def new_puzzle():
    return puzzle(words=[], positions=[["###"] * 15 for _ in range(15)])


def get_puzzle_piece(file, word_num):
    df_it = pd.read_csv(file, encoding="ISO-8859-1", chunksize=word_num)
    for chunk in enumerate(df_it):
        return chunk


def print_puzzle(crossword):
    print("*" * 60)
    print(crossword.words)
    print("*" * 60)
    for i in crossword.positions:
        for j in i:
            print(j, end="")
        print()

    print("*" * 60)


def check_and_add_word_to_position(cword, puz, intersection) -> bool:
    cur = cword.start
    for c in cword.word:
        if (
            cur[0] < 0
            or cur[0] >= len(puz.positions)
            or cur[1] < 0
            or cur[1] >= len(puz.positions[0])
        ):
            return False
        if puz.positions[cur[0]][cur[1]] != "###":
            if cur != intersection:
                return False
        if cword.vertical:
            cur = (cur[0] + 1, cur[1])
        else:
            cur = (cur[0], cur[1] + 1)
    cur = cword.start
    for c in cword.word:
        puz.positions[cur[0]][cur[1]] = f" {c} "
        if cword.vertical:
            cur = (cur[0] + 1, cur[1])
        else:
            cur = (cur[0], cur[1] + 1)
    return True


def can_it_fit(word, crossword):
    for i in range(len(word)):
        c = word[i]
        for cword in crossword.words:
            for j in range(len(cword.word)):
                char = cword.word[j]
                if c == char:
                    # check coords situation
                    if cword.vertical:
                        intersect = (cword.start[0] + j, cword.start[1])
                        new_start = (intersect[0], intersect[1] - i)
                        new_cword = CWord(
                            word=word,
                            start=new_start,
                            vertical=False,
                            question="Doesn't Matter",
                        )
                        ok = check_and_add_word_to_position(
                            new_cword, crossword, intersect
                        )
                        if ok:
                            crossword.words.append(new_cword)
                            return

                    else:
                        intersect = (cword.start[0], cword.start[1] + j)
                        new_start = (intersect[0] - i, intersect[1])
                        new_cword = CWord(
                            word=word,
                            start=new_start,
                            vertical=True,
                            question="Doesn't Matter",
                        )
                        ok = check_and_add_word_to_position(
                            new_cword, crossword, intersect
                        )
                        if not ok:
                            return
                        crossword.words.append(new_cword)
                        return


file = "nytcrosswords.csv"
piece = get_puzzle_piece(file, 5)
print(piece)

print("\n\n")

crossword = new_puzzle()
# cword = CWord(word="PAR", start=(5, 4), vertical=False, question="Doesn't Matter")
# crossword.words.append(cword)
# crossword.positions[5][4] = " P "
# crossword.positions[5][5] = " A "
# crossword.positions[5][6] = " R "
cword = CWord(word="PAR", start=(4, 5), vertical=True, question="Doesn't Matter")
crossword.words.append(cword)
crossword.positions[4][5] = " P "
crossword.positions[5][5] = " A "
crossword.positions[6][5] = " R "

# cword = CWord(word="BAD", start=(4, 3), vertical=True, question="Doesn't Matter")
# crossword.words.append(cword)
# crossword.positions[4][3] = " B "
# crossword.positions[5][3] = " A "
# crossword.positions[6][3] = " D "
print_puzzle(crossword)

can_it_fit("STAB", crossword)

print_puzzle(crossword)
