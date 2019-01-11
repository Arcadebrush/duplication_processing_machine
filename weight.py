# weight.py
import preprocessing

# caculate weight for each COMPANY
# logo, 한 줄 소개, 기업 소개 - 4
# name_ko, name_en, URL - 1
def Calculate_weight(LINE, iter, COMPANY_LIST):
    weight = 0

    # logo
    if int(LINE[8]) == 1:
        weight += 4

    if int(LINE[9]) == 1 or int(LINE[11]) == 1:
        weight += 4

    if int(LINE[10]) == 1 or int(LINE[12]) == 1:
        weight += 4

    [name_ko, name_en] = preprocessing.PREPROCESSING(iter, COMPANY_LIST)

    if name_ko:
        weight += 1

    if name_en:
        weight += 1

    if LINE[6]:
        weight += 1

    return weight
