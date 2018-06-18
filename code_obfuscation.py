#!/usr/bin/env python
# -*- coding: utf-8 -*-

from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit.ast import DotAccessor, Identifier, If

import sys
import bs4
from bs4 import BeautifulSoup


#functions are usually used for obfuscation
obfuscation_function_names = ['eval', 'replace', 'charCodeAt', 'fromCharCode', 'split', 'substr','unescape']

#user agent, app version, location, time,
profiling_function_names = ['navigator','userAgent','appVersion','appName',
                            'geolocation', 'Date', 'getTime', 'getMonth', 'getYear',
                            'getMinutes', 'getSeconds']


def inital_check_for_obfuscation_condtiion_sensitiveFunctions(js_text):
    parser = Parser()
    tree = parser.parse(js_text)

    keywords = set()
    if_condition = False

    for node in nodevisitor.visit(tree):

        if isinstance(node, If):
            if_condition = True
            continue

        stack = [node]

        #BFS to go to every depth of the AST tree
        while stack:
            node = stack.pop()
            #only dot access has a.b.getStringfromChar
            if isinstance(node, DotAccessor):
                try:
                    for i in node.children():
                        stack.append(i)
                except:
                    pass

                continue

            if isinstance(node, Identifier):
                #print (node.value),
                keywords.add(node.value)

    #print ("Done visit")
    obfuscation = False
    profiling = False

    if if_condition:
        pass

    ob_list = set()
    pro_list = set()

    for ob in obfuscation_function_names:
        if ob in keywords:
            #print ("[Obfuscation keywords]", ob)
            obfuscation = True
            ob_list.add(ob)
            #break

    for pro in profiling_function_names:
        if pro in keywords:
            #print ("[Profiling keywords]", pro)
            profiling = True
            pro_list.add(pro)
            #break

    #print ('if_condition: {}, obfuscation {}, profiling {}'.format(if_condition,obfuscation,profiling))
    #pint (js_text)
    return if_condition, obfuscation, profiling, ob_list, pro_list


def preprocess_check_for_url(url):
    with open(url, 'r') as myfile:
        data = myfile.read()

    try:
        data = data.decode('unicode_escape').encode('utf-8')

    except Exception as inst:
        data = None
        f = open('log-error.log','a')
        f.write("Data Encode Exception: " + str(type(inst)) + " " + str(url)+'\n')
        f.close()

    if data is None:

        return (None,None)

    soup = BeautifulSoup(data, "html.parser")
    scripts = soup.findAll("script")
    return (scripts, soup)


def ast_check_for_obfuscation_profiling(html_file):
    jss, _ = preprocess_check_for_url(html_file)
    ob = False
    pro = False

    if not jss:
        return False, False, set(), set()

    ob_set = set()
    pro_set = set()

    for js in jss:
        assert isinstance(js, bs4.element.Tag)

        if len(js.text) == 0:
            continue
        try:
            if_condition, obfuscation, profiling, ob_list_tmp, pro_list_tmp = inital_check_for_obfuscation_condtiion_sensitiveFunctions(js.text)
            ob = ob or obfuscation
            pro = pro or profiling

            ob_set.update(ob_list_tmp)
            pro_set.update(pro_list_tmp)

        except:
            #print ("AST breaks!")
            pass
            #obfuscation, profiling = True,True
    return ob, pro, ob_set, pro_set



#################### TEST ################
def test():
    html_file ="/home/ketian/Desktop/phishingdetect/groundTruth/1.mobile.source.txt"
    print (ast_check_for_obfuscation_profiling(html_file=html_file))


if __name__ == "__main__":
    test()