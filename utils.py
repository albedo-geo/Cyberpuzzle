import random
import rich
from typing import Any
import pyautogui
import time

__all__ = ['WORDS', "generate_puzzle", "print_puzzle", "print_path", "is_subsequence"]

WORDS = ['1C', '55', '7A', 'BD', 'E9', 'FF']


def generate_puzzle(
    size: int = 6, num_words: int = 5, seed: int = 1334
) -> list[list[str]]:
    """
    generate a puzzle with size * size cells
    """
    random.seed(seed)
    words = random.sample(WORDS, num_words)
    puzzle = [[random.choice(words) for _ in range(size)] for _ in range(size)]
    return puzzle


def print_puzzle(puzzle: list[list[str]]) -> None:
    """
    print the puzzle
    """
    for row in puzzle:
        print(' '.join(row))


def print_path(puzzle: list[list[str]], path: list[tuple[int, int]]) -> None:
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            if (x, y) == path[0]:
                rich.print(f'[red]{puzzle[y][x]}[/red]', end=' ')
            elif (x, y) in path:
                rich.print(f'[cyan]{puzzle[y][x]}[/cyan]', end=' ')
            else:
                print(puzzle[y][x], end=' ')
        print()


def is_subsequence(array: list[Any], sub: list[Any]) -> bool:
    """
    decide if sub is a subsequence of array
    """
    if not array or not sub:
        return False
    if array == sub:
        return True
    if len(array) < len(sub):
        return False
    for i in range(len(array)):
        for j in range(len(sub)):
            if i + j >= len(array):
                break
            if array[i + j] != sub[j]:
                break
            if j == len(sub) - 1:
                return True
    return False


def click_coors(coors, offset=(0, 0)):
    time.sleep(3)
    for coor in coors:
        coor = (coor[0] + offset[0], coor[1] + offset[1])
        pyautogui.moveTo(coor[0], coor[1], duration=0.35)
        pyautogui.click()
        print(coor)
        time.sleep(0.5)


if __name__ == '__main__':
    # a = [(1, 0), (0, 1), (0, 0), (1, 2)]
    # b = [(0, 1), (0, 0)]
    # print(is_subsequence(a, b))
    click_coors([[914, 570], [900, 1000], [1000, 1000], [1000, 900]])
