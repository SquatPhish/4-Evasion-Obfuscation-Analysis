#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ririhedou@gmail.com"

import os
import sys
import util_ke
import feature_extract


'''
In the base line, we implement the baseline p-hash
'''

try:
    import Image
except ImportError:
    from PIL import Image

import imagehash

import collections


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
    #print (type(hash))
    #width, height = im.size
    #print (width, height)
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

import shutil
def get_image_hash_comparison(brand ,phshing_id_labels, brand_labels):
    valid_id_list = brand_labels[str(brand)]

    crawl_dir = "/mnt/sdb1/browser_phishingTank/Crawl/" + brand + "/"

    target_web = "./groundTruth/" + brand + ".screen.png"
    target_mobile = "./groundTruth/" + brand + ".screen.png" #mobile

    web = list()

    print ("WEB BRAND {} {}".format(brand, util_ke.BrandMap[int(brand)].lower()))
    print (brand, len(valid_id_list))

    #for web
    p_web_basic = image_hash_computation(target_web)
    for i in valid_id_list:
        filename = crawl_dir + i + ".web.screen.png"
        try:
            p = image_hash_computation(filename)
            dif = p-p_web_basic
            #print (i, dif)
            web.append(dif)
        except:
            pass
            #print ("WTF web AT {}".format(i))


    print ("MOBILE")
    mobile = list()
    # for mobile
    p_mobile_basic = image_hash_computation(target_mobile)
    for i in valid_id_list:
        filename = crawl_dir + i + ".mobile.screen.png"
        try:
            p = image_hash_computation(filename)
            dif = p - p_mobile_basic
            #print (i, dif)
            mobile.append(dif)
        except:
            pass
            #print ("WTF mobile AT {}".format(i))

    print ("WEB IMAGE", len(web))
    print ("Average", sum(web)/len(web))
    print (web)
    print ("MOBILE IMAGE", len(mobile))
    print (mobile)
    print ("Average", sum(mobile) / len(mobile))
    #import graph_ke
    #graph_ke.p_hash_distribution(web, mobile, title=util_ke.BrandMap[int(brand)])
    return web, mobile



def get_string_obfuscation(brand, phshing_id_labels, brand_labels):
    valid_id_list = brand_labels[str(brand)]

    print (brand, len(valid_id_list))

    brand_string = util_ke.BrandMap[int(brand)].lower()
    base = "./groundTruth/" + brand + ".source.txt"
    text_word_str, num_of_forms, attr_word_str = feature_extract.get_structure_html_text(base)
    parts = text_word_str.lower().split()

    print (text_word_str)
    if any(brand_string == p for p in parts):
        print ("YES, can findin official website")
    else:
        print ("NO")


    same = 0
    not_same = 0
    crawl_dir = "/mnt/sdb1/browser_phishingTank/Crawl/" + brand + "/"
    web_cannot_find = list()
    not_found, found = 0, 0
    exist_id_to_url_mapping = search_database_for_url(brand)
    squatting_urls = [line.strip() for line in open("SQUAT_EX_POP").readlines()]

    for i in valid_id_list:

        url = exist_id_to_url_mapping[i]
        if url in squatting_urls:
            print ("FFFFFFF")
            sys.exit()


        html = crawl_dir + i + ".web.source.html"
        mb_html =  crawl_dir + i + ".mobile.source.html"

        text_word_str, num_of_forms, attr_word_str = feature_extract.get_structure_html_text(html)
        text_word_str2, num_of_forms2, attr_word_str2 = feature_extract.get_structure_html_text(mb_html)
        if text_word_str == text_word_str2 and attr_word_str2 == attr_word_str:
            same +=1
        else:
            not_same+= 1
            #print (i)
            #raw_input()

        parts = text_word_str.lower().split()

        if any(brand_string == p for p in parts):
            found += 1
        else:
            not_found += 1
            web_cannot_find.append(i)
        #print (i, brand)

    print ("Brand string", brand_string)
    print ("Web total {},  found {}, not found {}".format(found+not_found,found, not_found))
    #print ("same", same , "not same", not_same)
    return same, not_same
    """
    not_found, found = 0, 0
    mobile_cannot_find = list()
    for i in valid_id_list:
        html = crawl_dir + i + ".mobile.source.html"
        text_word_str, num_of_forms, attr_word_str = feature_extract.get_structure_html_text(html)
        parts = text_word_str.lower().split()

        if any(brand_string == p for p in parts):
            found += 1
        else:
            not_found += 1
            mobile_cannot_find.append(i)
            # print (i, brand)

    print ("Brand string", brand_string)
    print ("Mobile total {},  found {}, not found {}".format(found + not_found, found, not_found))
    print ("Analysis")
    if len(web_cannot_find) == len(mobile_cannot_find):
        return
    else:
        for i in mobile_cannot_find:
            if i not in web_cannot_find:
                print ("FUCK", i)
                raw_input()

    """

def source_code_obfuscation(brand, phshing_id_labels, brand_labels):

    valid_id_list = brand_labels[str(brand)]

    print (brand, len(valid_id_list))

    brand_string = util_ke.BrandMap[int(brand)].lower()
    base = "./groundTruth/" + brand + ".source.txt"
    import code_obfuscation


    crawl_dir = "/mnt/sdb1/browser_phishingTank/Crawl/" + brand + "/"

    #html = crawl_dir + "5457206" + ".web.source.html"
    #p = code_obfuscation.ast_check_for_obfuscation_profiling(html)
    #print (p)
    #return

    ob_list = list()
    pro_list = list()
    ob_dict = collections.defaultdict(int)
    pro_dict = collections.defaultdict(int)


    for i in valid_id_list:
        #print ("ID is {}".format(i))
        html = crawl_dir + i + ".web.source.html"
        obfuscation, profiling, obset, proset = code_obfuscation.ast_check_for_obfuscation_profiling(html)

        ob_list.append(obfuscation)
        pro_list.append(profiling)

        for i in obset:
            ob_dict[i] += 1
        for i in proset:
            pro_dict[i] += 1

    print ("=================== WEB ======================")
    print ("TOTAL",  len(ob_list), len(pro_list))
    ob_count = sum(1 for i in ob_list if i)
    pro_count = sum(1 for i in pro_list if i)
    print ("BRAND/OB_count/Pro_count", util_ke.BrandMap[int(brand)], ob_count, pro_count)
    print ("BRAND TOTAL", len(valid_id_list))
    print ("BRAND", util_ke.BrandMap[int(brand)], (ob_count+0.0)/len(valid_id_list), (pro_count+0.0)/len(valid_id_list) )
    print ("OB", util_ke.BrandMap[int(brand)],ob_dict)
    print ("PRO", util_ke.BrandMap[int(brand)],pro_dict)

    ob_list = list()
    pro_list = list()
    ob_dict = collections.defaultdict(int)
    pro_dict = collections.defaultdict(int)

    for i in valid_id_list:
        # print ("ID is {}".format(i))
        html = crawl_dir + i + ".mobile.source.html"
        obfuscation, profiling, obset, proset = code_obfuscation.ast_check_for_obfuscation_profiling(html)

        ob_list.append(obfuscation)
        pro_list.append(profiling)

        for i in obset:
            ob_dict[i] += 1
        for i in proset:
            pro_dict[i] += 1

    print ("=================== MOBILE ======================")
    print ("TOTAL", len(ob_list), len(pro_list))
    ob_count = sum(1 for i in ob_list if i)
    pro_count = sum(1 for i in pro_list if i)
    print ("BRAND/OB_count/Pro_count", util_ke.BrandMap[int(brand)], ob_count, pro_count)
    print ("BRAND TOTAL", len(valid_id_list))
    print ("BRAND", util_ke.BrandMap[int(brand)], (ob_count + 0.0) / len(valid_id_list),
           (pro_count + 0.0) / len(valid_id_list))
    print ("OB", util_ke.BrandMap[int(brand)], ob_dict)
    print ("PRO", util_ke.BrandMap[int(brand)], pro_dict)


import csv
def get_squat_analysis_on_urls(brand):
    DATABASE_DIR = "/mnt/sdb1/browser_phishingTank/database/"
    csv_brand = DATABASE_DIR + brand +".csv"

    cur_folder = "/mnt/sdb1/browser_phishingTank/Crawl/" + brand + "/"
    cans = util_ke.read_pngs_sources_from_directory(cur_folder)


    keys = [i.idx for i in cans]
    print (brand, len(keys))
    urls = list()
    with open(csv_brand, "rb") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            idx = line[0]
            url = line[1]
            if idx in keys:
                urls.append(url)

    print (len(urls))
    f = open('LIST_' + brand , 'w+')
    for i in urls:
        f.write(i + '\n')
    return len(keys)


def search_database_for_url(_id):
    DATABASE_DIR = "/mnt/sdb1/browser_phishingTank/database/"  # we set global output dir
    database = DATABASE_DIR + str(_id) + '.csv'
    exist_indexes = dict()
    if os.path.exists(database):
        with open(database, 'r') as userFile:
            userFileReader = csv.reader(userFile)
            for row in userFileReader:
                exist_indexes[row[0]] = row[1]

    return exist_indexes


if __name__ == "__main__":
    brands = ["1","2","74","76","177","207", "109", "194"]
    brands = ["1", "2", "74", "76", "177", "207", "109", "194"]

    #brand = "74"
    #get_squat_analysis_on_urls(brand)

    #source_code_obfuscation(brand)
    #sys.exit(0)

    #j = 0
    phshing_id_labels, brand_labels = util_ke.load_relabeled()
    #get_image_hash_comparison("1",phshing_id_labels, brand_labels)

    #get_string_obfuscation("74", phshing_id_labels, brand_labels)

    print (brand_labels["1"])
    s = 0
    ns = 0
    for brand in brands:
        #i = get_squat_analysis_on_urls(brand)
        #j = j + i
        #print (j)
        #a, b = get_image_hash_comparison(brand,phshing_id_labels, brand_labels)
        #print (a,b)
        #source_code_obfuscation(brand,phshing_id_labels, brand_labels)
        _s, _ns = get_string_obfuscation(brand, phshing_id_labels, brand_labels)
        s += _s
        ns += _ns

    print (s/(s+ns+0.0))

    #web, brand = get_perception_hash_comparison(brand)
    #for brand in brands:
    #    get_string_obfuscation(brand)
    #print (web)
    #print (brand)

    #p2 = p_hash_computation(img2)
    #print (p1-p2)
    #print (p2-p1)
    #img = "/home/ketian/Desktop/phishingdetect/groundTruth/1.screen.png"
    #img2 = "/home/ketian/Desktop/phishingdetect/labeled_data/web_Y/1264593.web.screen.png"

    #p1 =image_hash_computation("/home/ketian/Desktop/phishingdetect/groundTruth/1.screen.png")
    #print (p1)

    #p3 = image_hash_computation("/mnt/sdb1/browser_phishingTank/Crawl/8/5532694.web.screen.png")
    #print (p3)
    #print (p1-p3)
