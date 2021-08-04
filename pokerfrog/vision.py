"""Module to work with computer vision."""

import csv
import functools
import os
from typing import Optional

import numpy as np
from PIL import ImageDraw, ImageGrab

import cv2
import pyautogui
from pokerfrog.domain import CARD_SUITS, CARD_VALUES, Card


@functools.lru_cache(maxsize=1)
def read_csv_labels(filepath):
    """Return dict with label and it's metadata."""
    cols = [
        'label',
        'left',
        'top',
        'width',
        'height',
        'img',
        'img_width',
        'img_height',
    ]

    res = {}
    with open(filepath, 'r', encoding='utf-8') as csv_file:
        for label in csv.DictReader(csv_file, delimiter=',', fieldnames=cols):
            res[label['label']] = label

    return res


def get_images_from_labels(im, labels):
    """Return dict with pairs of (label, Pillow Image) from labels list."""
    rects = {}

    for label, bounds in labels.items():
        left, top = int(bounds['left']), int(bounds['top'])
        width, height = int(bounds['width']), int(bounds['height'])

        rects[label] = (left, top, left+width, top+height)

    res = {}
    for label, rect in rects.items():
        res[label] = im.crop(rect)

    return res


@functools.lru_cache(maxsize=1)
def load_cv2_templates(dirpath):
    """Load card values and suits templates as list of cv2 images."""
    res = {}
    for filename in os.listdir(dirpath):
        temlate_name, _ = filename.split('.', 1)

        res[temlate_name] = cv2.imread(os.path.join(dirpath, filename), 0)

    return res


def _get_best_cv2_template_match(image_cv, templates):
    res_str, best_score = None, 0.75
    for label, template in templates.items():
        res = cv2.matchTemplate(image_cv, template, cv2.TM_CCOEFF_NORMED)
        score = res.max()

        if score > best_score:
            res_str, best_score = label, score

    return res_str


def image_to_card(im, templates) -> Optional[Card]:
    """Convert Pillow Image to optional Card class from domain module."""
    width, height = im.size
    SPLIT_HEIGHT = 22

    value_im = im.crop((0, 0, width, SPLIT_HEIGHT))
    suit_im = im.crop((0, SPLIT_HEIGHT, width, height))

    value_cv = cv2.cvtColor(np.array(value_im), cv2.COLOR_RGB2GRAY)
    value_templates = {key: templates[key] for key in CARD_VALUES}
    value_str = _get_best_cv2_template_match(value_cv, value_templates)

    suit_cv = cv2.cvtColor(np.array(suit_im), cv2.COLOR_RGB2GRAY)
    suit_templates = {key: templates[key] for key in CARD_SUITS}
    suit_str = _get_best_cv2_template_match(suit_cv, suit_templates)

    if not all([value_str, suit_str]):
        return None

    return Card(value_str, suit_str)


def get_hand_and_table(im):
    templates = load_cv2_templates('./assets/poker_stars/cards/')
    labels = read_csv_labels('./assets/poker_stars/players_6.csv')
    images = get_images_from_labels(im, labels)

    table, hand = [], []
    for key in ['card1', 'card2', 'card3', 'card4', 'card5', 'hand1', 'hand2']:
        card = image_to_card(images[key], templates)

        if key.startswith('card'):
            table.append(card)
        else:
            hand.append(card)

    return hand, table
