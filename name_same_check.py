# -*- coding:utf-8 -*-

'''
    두어진 2개의 회사의 이름이 동일한지 확인해 본다.
'''

from preprocessing import PREPROCESSING
from translation import translate

def Is_same(Com1_list, Com2_list):

    # remove ""
    while "" in Com1_list:
        Com1_list.remove("")

    while "" in Com2_list:
        Com2_list.remove("")

    # find common elements
    # common elements mean their names are same
    Com1_set = set(Com1_list)
    Com2_set = set(Com2_list)

    if Com1_set & Com2_set:
        return True

    else:
        return False



# compare COMPANY_LIST[iterator1] and COMPANY_LIST[iterator2]
def name_same_check(name_ko, name_en, translation_name, iterator2, COMPANY_LIST):

    # preprocessing for Company_2
    [iter2_name_ko, iter2_name_en] = PREPROCESSING(iterator2, COMPANY_LIST)

    # translation_name for Company_2
    tr_name = list(COMPANY_LIST[iterator2][13])

    # inclusive and exact matching
    # <로켓펀치, rocketpunch> and <로켓펀치(rocketpunch), > - inclusive

    name_list1 = [name_ko, name_en,name_ko + name_en, name_en + name_ko] + translation_name
    name_list2 = [iter2_name_ko, iter2_name_en, iter2_name_ko + iter2_name_en, iter2_name_en + iter2_name_ko] + tr_name

    if Is_same(name_list1, name_list2):
        return True

    return False
