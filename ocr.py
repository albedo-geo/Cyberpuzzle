from black import main
import easyocr
from PIL import Image, ImageDraw, ImageGrab
import numpy as np
import json
from utils import print_puzzle, print_path, click_coors, WORDS
from solver import find_best_path


def save_json(obj, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4)


def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)


def ocr(img, thres=0.5, scale=1.0):
    reader = easyocr.Reader(['en'], gpu=False)
    boxes = reader.readtext(
        img, allowlist='1C7ABD5E9F', mag_ratio=scale, width_ths=1.25
    )
    results = []

    for box in boxes:
        [[a, b], _, [e, f], _], text, p = box
        if p < thres:
            continue
        results.append((((a.item(), b.item()), (e.item(), f.item())), text, p))

    return results


def visualize(img, results, offset=None):
    draw = ImageDraw.Draw(img)
    for box, text, p in results:
        if offset is not None:
            offset = np.asarray(offset)
            box = [tuple(np.asarray(t) + offset) for t in box]
        box = [tuple(i) for i in box]
        draw.rectangle(box, outline='red')
        draw.text(box[0], text, fill='red')
    img.show()


def results_to_matrix(results):
    x_thres = 700
    lefts = []
    rights = []
    for coor, text, _ in results:
        if coor[0][0] < x_thres:
            lefts.append((coor, text))
        else:
            rights.append((coor, text))

    # lefts
    lefts = sorted(lefts, key=lambda r: r[0][0][1])
    puzzle = []
    coors = []
    for coor, text in lefts:
        if len(text) < 10:
            continue
        words = []
        for i in range(0, len(text) - 1, 2):
            words.append(text[i : i + 2])
        puzzle.append(words)
        # get coors
        side_len = coor[1][1] - coor[0][1]
        left_coor = coor[0][0] + side_len // 2
        right_coor = coor[1][0] - side_len // 2
        y = coor[0][1] + side_len // 2
        x_interval = (right_coor - left_coor) // (len(lefts) - 1)
        row_coors = [(left_coor + i * x_interval, y) for i in range(len(lefts))]
        coors.append(row_coors)

    print_puzzle(puzzle)

    # rights
    rights = sorted(rights, key=lambda r: r[0][0][1])
    objectives = []
    for coor, text in rights:
        if len(text) < 5:
            continue
        words = []
        isvalid = True
        for i in range(0, len(text) - 1, 2):
            word = text[i : i + 2]
            if word not in WORDS:
                isvalid = False
                break
            words.append(word)
        if isvalid:
            objectives.append(words)
    print(objectives)

    return puzzle, objectives, coors


def main():
    # img_path = 'img/screenshot.jpg'
    # img = Image.open(img_path)
    img = ImageGrab.grabclipboard()
    # crop_range = [145, 330, 1260, 800]
    # crop = np.asarray(img.crop(crop_range))
    results = ocr(np.asarray(img))
    # save_json(results, 'results.json')
    # results = load_json('results.json')
    matrix, objs, coors = results_to_matrix(results)
    # visualize(img, results, [0, 0])
    _, path = find_best_path(matrix, objs, 8)
    print_path(matrix, path)
    # click_coors([coors[i][j] for i, j in path], offset=(613, 157))


if __name__ == '__main__':
    main()
    # ImageGrab.grabclipboard().show()
