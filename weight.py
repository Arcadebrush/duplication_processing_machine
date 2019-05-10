# -*- coding:utf-8 -*-
'''
    기업의 가중치를 계산한다.
'''

# caculate weight for each COMPANY
# logo, 한 줄 소개, 기업 소개 - 4
# name_ko, name_en, URL - 1
def Calculate_weight(LINE):
    weight = 0

    # 기업 로고
    if int(LINE[6]) == 1:
        weight += 4

    # 한 줄 소개
    if int(LINE[7]) ==  1 or int(LINE[9]) == 1:
        weight += 4

    # 기업 소개
    if int(LINE[8]) == 1 or int(LINE[10]) == 1:
        weight += 4

    name_ko = LINE[1]
    name_en = LINE[2]

    if name_ko:
        weight += 1

    if name_en:
        weight += 1

    # 기업 URL
    if LINE[4]:
        weight += 1

    return weight
