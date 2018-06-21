#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ririhedou@gmail.com"

import os

import code_obfuscation
import feature_extract

try:
    import Image
except ImportError:
    from PIL import Image

import imagehash


def image_hash_computation(img):
    im = Image.open(img)
    """
    tmp = img.split('/')[-1] + ".png"
    print (tmp)

    new_width = 500
    new_height = 500
    img = im.resize((new_width, new_height), Image.ANTIALIAS)
    img.save(tmp)
    im = Image.open(tmp)
    """
    hash = imagehash.average_hash(im)

    #hash = imagehash.phash(im)

    return hash


def read_images_from_a_folder(folder):
    def is_image(filename):
        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or \
               f.endswith(".jpeg") or f.endswith(".bmp") or f.endswith(".gif")

    arr = os.listdir(folder)
    if not folder.endswith('/'):
        folder = folder + '/'

    imgs = set()
    for f in arr:
        if is_image(f):
            imgs.add(folder + f)
    return list(imgs)


def get_image_hash_comparison(img1, img2):
    p1 = image_hash_computation(img1)
    p2 = image_hash_computation(img2)
    hash_dis = p1 -p2
    print ("Image hash distance is {}".format(hash_dis))
    return


def get_string_obfuscation(brand_string, html):
    text_word_str, num_of_forms, attr_word_str = feature_extract.get_structure_html_text(html)

    brand_string = brand_string.lower()
    parts = text_word_str.lower().split()

    #print (text_word_str)
    if any(brand_string == p for p in parts):
        print ("NO Obfuscated, can find in the website")
    else:
        print ("Obfuscated, cannot find the string")


def source_code_obfuscation(html):

    obfuscation, profiling, obset, proset = code_obfuscation.ast_check_for_obfuscation_profiling(html)

    #ob, pro, ob_set, pro_set
    if obfuscation:
        print ("obfuscation detected")

    if profiling:
        print ("profiling detected")

    return


if __name__ == "__main__":
    pass