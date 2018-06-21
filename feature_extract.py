#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract
from bs4 import BeautifulSoup

# import nltk - a library for NLP analysis
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import tag
from autocorrect import spell
from sys import platform


import WORD_TERM_KEYS
import re
import os
import codecs


WORD_TERM = WORD_TERM_KEYS.WORD_TERM

if platform == "linux" or platform == "linux2":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
elif platform == "darwin":
    # OS X
    pytesseract.pytesseract.tesseract_cmd = "/usr/local/bin/tesseract"
elif platform == "win32":
    # Win
    print ("please specify the path")
    # Include the above line, if you don't have tesseract executable in your PATH
    # Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'


def get_img_text_ocr(img_path):
    """
    :param img_path:
    :return:
    This part is to extract words from an image. We apply OCR technique to read texts from images.
    More info on OCR can be found:
    https://github.com/madmaze/pytesseract
    """
    img = Image.open(img_path)
    text = pytesseract.image_to_string(img, lang='eng')
    sent = word_tokenize(text.lower())
    words = [word.lower() for word in sent if word.isalpha()]

    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    ocr_text = ' '.join(words)
    return ocr_text


def get_img_text_from_ocr_txt(img_txt_path):
    text = ''
    f = codecs.open(img_txt_path, 'r', encoding='utf-8')
    for line in f.readlines():
        line = line.strip()
        text += ' ' + line
    f.close()
    sent = word_tokenize(text.lower())
    words = [word.lower() for word in sent if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]
    ocr_text = ' '.join(words)
    return ocr_text


def get_structure_html_text(html_path):
    """
    :param html_path:
    :return:
    """
    data = codecs.open(html_path, 'r', encoding='utf-8').read()
    try:
        soup = BeautifulSoup(data, "lxml")
    except Exception as inst:
        f = open('log-error.log', 'a')
        f.write("SoupParse Exception: " + str(type(inst)) + " " + str(html_path) + '\n')
        f.close()
        return None, None, None

    heads = '.'.join(t.text for t in soup.find_all(re.compile(r'h\d+')))
    things = '.'.join(p.text for p in soup.find_all('p'))
    tags = '.'.join(a.text for a in soup.find_all('a'))
    titles = '.'.join(t.text for t in soup.find_all('title'))

    raw = heads + ' ' + things + ' ' + tags + ' ' + titles
    sent = word_tokenize(raw)
    #tokenize html

    tokens = tag.pos_tag(sent)
    #_map = {i.lower():j for i,j in tokens}
    #remove no-alpha words

    words = [word.lower() for word, _ in tokens if word.isalpha()]
    #words = list(set(words))

    #remove stop words
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if w not in stop_words]

    text_word_str = ' '.join(words)

    #form analysis
    forms = soup.find_all('form')
    num_of_forms = len(forms)
    candidate_attributes = ['type', 'name', 'submit', 'placeholder']
    attr_word_list = list()

    for idx, form in enumerate(forms):
        inputs = form.find_all('input')
        for i in inputs:
            for j in candidate_attributes:
                if i.has_attr(j):
                    attr_word_list.append(i[j])

    attr_word_str = ' '.join(attr_word_list)

    words = word_tokenize(attr_word_str)
    words = [word.lower() for word in words if word.isalpha()]

    # words = list(set(words))
    # remove stop words
    words = [w for w in words if w not in stop_words]
    attr_word_str = ' '.join(words)

    return text_word_str, num_of_forms, attr_word_str


def text_embedding_into_vector(txt_str):
    """
    :param text_str:
    :return:
    We split text into a list of features for training
    """
    texts = txt_str.split(' ')
    texts = [spell(w).lower() for w in texts]
    embedding_vector = [0]*(len(WORD_TERM) + 1)
    for elem in texts:
        # if it exist, we set the index plus one
        # else the last position plus one
        index = WORD_TERM.index(elem) if elem in WORD_TERM else -1
        embedding_vector[index] += 1

    return embedding_vector


def feature_vector_extraction(candidate):
    """
    :param candidate: a candidate object
    :return: the feature vector
    it consists of three components: img-text, html-text, form-text
    """
    print ("Analyse source and image at:")
    print (candidate.source_html)
    print (candidate.img_path)

    if os.path.exists(candidate.source_html) and os.path.exists(candidate.img_path):
        try:
            img_text = get_img_text_ocr(candidate.img_path)

            #print (img_text)

            if len(img_text) == 0:
                return None

            text_word_str, num_of_forms, attr_word_str = get_structure_html_text(candidate.source_html)
            img_v = text_embedding_into_vector(img_text)
            txt_v = text_embedding_into_vector(text_word_str)
            form_v = text_embedding_into_vector(attr_word_str)
            final_v = img_v + txt_v + form_v + [num_of_forms]
            return final_v

        except:

            print ("error happened! maybe your img/html-source format is not acceptable?")
            return None


def feature_vector_extraction_from_img_html(img, html):

    if os.path.exists(img) and os.path.exists(html):
        print ("Img is {}".format(img))
        print ("HTML is {}".format(html))
        try:
            img_text = get_img_text_ocr(img)

            if len(img_text) == 0:
                return None

            text_word_str, num_of_forms, attr_word_str = get_structure_html_text(html)

            img_v = text_embedding_into_vector(img_text)
            txt_v = text_embedding_into_vector(text_word_str)
            form_v = text_embedding_into_vector(attr_word_str)
            final_v = img_v + txt_v + form_v + [num_of_forms]

            return final_v

        except:

            print ("error happened! maybe your format is not acceptable?")
            return None
    else:
        print ("Not exist path")
        return None


if __name__ == "__main__":

    img = "./test/facebook-c.com.screen.png"
    img = os.getcwd() + "/test/facebook-c.com..screen.png"
    source = os.getcwd() + "/test/facebook-c.com..source.txt"

    v = feature_vector_extraction_from_img_html(img=img, html=source)
    print ("The feature vector is")
    print (v)


