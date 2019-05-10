# -*- coding:utf-8 -*-
'''
    로켓펀치 기업데이터의 이름과 다른 정보를 가지고서 중복테스트를 진행한다.
'''

import os, sys
from weight import Calculate_weight
from preprocessing import PREPROCESSING, PREPROCESSING_FOR_NAME
from name_same_check import name_same_check
from validation_test import validation_test
from connect import Connect_data
from translation import translate

# FILE NAME
FILE_NAME = "company20190417_test"

# write_file
def write_file(__filename__, COMPANY_LIST):
    file = open(__filename__, "w")

    for iter in range(len(COMPANY_LIST)):
        for idx in range(len(COMPANY_LIST[iter])-1):
            file.write(str(COMPANY_LIST[iter][idx]) + "\t")

        file.write("\n")

    file.close()


# load company data
def data_loading(__filename__, COMPANY_LIST, CORRECT_DATA, INCORRECT_DATA):
    try :
        with open("same_data","r") as cor_data:
            for data in cor_data.readlines():
                data = data.strip().split("\t")

                CORRECT_DATA.append(set(data))

    except IOError:
        with open("same_data","w") as cor_data:
            pass
    try :
        with open("different_data","r") as cor_data:
            for data in cor_data.readlines():
                data = data.strip().split("\t")

                INCORRECT_DATA.append(set(data))

    except IOError:
        with open("different_data","w") as cor_data:
            pass


    with open(__filename__, 'r') as datafile:


        for line in datafile.readlines():
            # avoid overlapping
            line = line.strip().split('\t')

            # if line doesn't have weight yet
            if len(line) < 12:
                line.append(Calculate_weight(line))

            # 이 기업이 테스트 되었는지 안 되었는지 확인
            # 0 -> 안되었음
            # 1 -> 되었음
            if len(line) < 13:
                line.append("0")

            # line에 translation_list를 붙인다.
            name_ko, name_en = PREPROCESSING_FOR_NAME(line[1], line[2])
            line.append(translate([name_ko, name_en]))

            # push back
            COMPANY_LIST.append(line)


    print("loading " + str(__filename__) + " data is done successfully!")

    # write_file
    write_file(__filename__, COMPANY_LIST)

    return COMPANY_LIST, CORRECT_DATA,INCORRECT_DATA

if __name__=="__main__":

    # 기업의 정보가 들어갈 LIST
    COMPANY_LIST = []

    # 동일한 기업의 정보가 (id, id) 형태의 LIST로 저장
    # index는 불러오는 파일의 구조에 따라 달라진다.
    CORRECT_DATA = []

    # 다른 기업의 정보가 (id, id) 형태의 LIST로 저장
    INCORRECT_DATA = []

    # __filename__
    [COMPANY_LIST,CORRECT_DATA,INCORRECT_DATA] = data_loading(FILE_NAME, COMPANY_LIST, CORRECT_DATA, INCORRECT_DATA)

    try :
        for iter_1, com_data_list in enumerate(COMPANY_LIST):

            # 이미 체크한 것 안하도록
            if com_data_list[12] != "0":
                continue

            [name_ko, name_en] = PREPROCESSING(iter_1, COMPANY_LIST)

            # 한글 - 로마자 번역 필요
            translation_name = list(com_data_list[13])

            for iter_2 in range(iter_1 + 1, len(COMPANY_LIST)):
                # if name is same with [name_ko, name_en]
                if name_same_check(name_ko, name_en, translation_name, iter_2, COMPANY_LIST):
                    '''
                    # It is already in Same_data file
                    if set([COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]]) in CORRECT_DATA:
                        pass
                    '''

                    # It is already in Different_data file
                    if set([COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]]) in INCORRECT_DATA:
                        pass

                    # Check Company_1 and Company_2 are really same
                    elif validation_test(iter_1, iter_2, COMPANY_LIST):
                        with open("same_data","a") as file:
                            file.write("{0}\t{1}\n".format(COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]))
                    else:
                        with open("different_data","a") as file:
                            file.write("{0}\t{1}\n".format(COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]))

            com_data_list[12] = "1"

        write_file(FILE_NAME, COMPANY_LIST)
        print("Checking done successfully!\n\nData Conneting...")
        Connect_data(COMPANY_LIST)
        print("DATA connecting Done!")

    except:
        write_file(FILE_NAME, COMPANY_LIST)
        print("\nSaved! and Exit!")
