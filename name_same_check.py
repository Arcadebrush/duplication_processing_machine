# -*- coding:utf-8 -*-
# name_same_check
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from google.cloud import translate
from preprocessing import PREPROCESSING
from levenshtein import levenshtein

# Instantiates a client
# translate_client = translate.Client()

# compare COMPANY_LIST[iterator1] and COMPANY_LIST[iterator2]
def name_same_check(name_ko, name_en, translation_name, iterator2, COMPANY_LIST):

    # preprocessing
    [iter2_ko_name, iter2_en_name] = PREPROCESSING(iterator2, COMPANY_LIST)

    tr_name = ""

    # inclusive
    # <로켓펀치, rocketpunch> and <로켓펀치(rocketpunch), >
    if name_ko and name_en:
        if (name_ko + name_en == iter2_ko_name) or (name_en + name_ko == iter2_ko_name):
            return True
        if (name_ko + name_en == iter2_en_name) or (name_en + name_ko == iter2_en_name):
            return True

    if iter2_ko_name and iter2_en_name:
        if (iter2_ko_name + iter2_en_name == name_ko) or (iter2_en_name + iter2_ko_name == name_ko):
            return True
        if (iter2_ko_name + iter2_en_name == name_en) or (iter2_en_name + iter2_ko_name == name_en):
            return True

    # if words distance is less than 2
    # exact matching

    if name_ko:
        if iter2_ko_name and name_ko == iter2_ko_name:
            return True

        if iter2_en_name and name_ko == iter2_en_name:
            return True

        if tr_name and name_ko == tr_name:
            return True

    if name_en:
        if iter2_ko_name and name_en == iter2_ko_name:
            return True

        if iter2_en_name and name_en == iter2_en_name:
            return True

        if tr_name and name_en == tr_name:
            return True

    if translation_name:
        if iter2_ko_name and translation_name == iter2_ko_name:
            return True

        if iter2_en_name and translation_name == iter2_en_name:
            return True

        if tr_name and translation_name == tr_name:
            return True

    return False
