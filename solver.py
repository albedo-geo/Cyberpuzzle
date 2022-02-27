from utils import *


def solve_puzzle(puzzle: list[list[str]], target: list[str], max_steps: int):
    """
    solve the puzzle
    """
    size = len(puzzle)

    def dfs(pos: tuple[int, int], direction: bool, path: list[tuple[int, int]]) -> None:
        current = [puzzle[i][j] for j, i in path]
        if is_subsequence(current, target):
            print(path, current)
            return
        if len(path) > max_steps:
            return

        x, y = pos

        for i in range(size):
            if direction:
                p = (i, y)
            else:
                p = (x, i)
            if p in path:
                continue
            path.append(p)
            dfs(p, not direction, path)
            path.pop()

    dfs((-1, 0), True, [])


def find_best_path(puzzle: list[list[str]], targets: list[list[str]], max_steps: int):
    """
    find the best path

    best path:
    1. highest score
    2. shortest path
    """
    size = len(puzzle)
    cur_max = 0
    res_path = []

    max_pos_score = sum(i + 1 for i in range(len(targets)))

    def dfs(pos: tuple[int, int], direction: bool, path: list[tuple[int, int]]) -> None:
        nonlocal cur_max, res_path

        if path:
            # the current sequence decided by the path
            current = [puzzle[i][j] for j, i in path]
            score = 0
            # calculate the current score gained within this path
            for s, t in enumerate(targets):
                if is_subsequence(current, t):
                    score += s + 1
            if score > 0:
                # if the current path is a relatively better solution
                if score > cur_max or score == cur_max and len(path) < len(res_path):
                    cur_max = score
                    res_path = path.copy()
            # if this path has already got the highest possible score,
            # then there is no need to go further
            if score == max_pos_score:
                return
            if len(path) >= max_steps:
                return

        x, y = pos

        for i in range(size):
            p = (i, y) if direction else (x, i)
            if p not in path:
                # backtracking
                path.append(p)
                dfs(p, not direction, path)
                path.pop()

    dfs((-1, 0), True, [])

    return cur_max, res_path


if __name__ == '__main__':
    puzzle = generate_puzzle(6, 5, 1334)
    targets = [['1C', 'E9'], ['E9', 'FF', 'BD'], ['BD', 'E9', '1C']]
    print_puzzle(puzzle)
    score, path = find_best_path(puzzle, targets, 7)
    print(path)
    print_path(puzzle, path)
