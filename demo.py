#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ririhedou@gmail.com"

import os
import evasion_analysis


def main():
    ground_fb = os.getcwd() + "/groundTruth/74.screen.png"
    p1 = os.getcwd() + "demo/faceb00k-bid-web.png"
    dis = evasion_analysis.get_image_hash_comparison(ground_fb, p1)
    print (dis)


main()