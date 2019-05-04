# -*- coding:utf-8 -*-
# duplication_test_machine_ver_0.1

# pip install --upgrade google-cloud-translate
import os, sys
from google.cloud import translate

# Instantiates a client
#translate_client = translate.Client()

import weight
from preprocessing import PREPROCESSING
from name_same_check import name_same_check
from validation_test import validation_test, information, COMPANY_TAG_PAGE_TEST
from merge import merge

# TEST FILE
FILE_NAME = "company20190417"

# write_file
def write_file(__filename__, COMPANY_LIST):
    file = open(__filename__, "w")

    for iter in range(len(COMPANY_LIST)):
        for data in COMPANY_LIST[iter]:
            file.write(str(data) + "\t")

        file.write("\n")

    file.close()

# load company data
def data_loading(__filename__, COMPANY_LIST, CORRECT_DATA, INCORRECT_DATA):
    with open("correct_data_backup","r") as cor_data:
        for data in cor_data.readlines():
            data = data.strip().split("\t")

            CORRECT_DATA.append(set(data))

    with open("name_same_but_different","r") as cor_data:
        for data in cor_data.readlines():
            data = data.strip().split("\t")

            INCORRECT_DATA.append(set(data))


    with open(__filename__, 'r') as datafile:

        iterator = 0

        for line in datafile.readlines():
            # avoid overlapping
            line = line.strip().split('\t')

            # push back
            COMPANY_LIST.append(line)

            # if line doesn't have weight yet
            if len(line) < 12:
                # DEBUG:
                # print(iterator)
                COMPANY_LIST[iterator].append(weight.Calculate_weight(line, iterator, COMPANY_LIST))

            # if line doesn't have connected_with yet
            # it means it is not checked_yet
            if len(line) < 13:
                COMPANY_LIST[iterator].append("-1")

            iterator += 1


    print("loading " + str(__filename__) + " data is done successfully!")

    # write_file
    write_file(__filename__, COMPANY_LIST)

    return COMPANY_LIST, CORRECT_DATA,INCORRECT_DATA

if __name__=="__main__":

    COMPANY_LIST = []
    CORRECT_DATA = []
    INCORRECT_DATA = []

    # __filename__
    [COMPANY_LIST,CORRECT_DATA,INCORRECT_DATA] = data_loading(FILE_NAME, COMPANY_LIST, CORRECT_DATA, INCORRECT_DATA)

    # time_complexity O(N^2)
    for iter_1, data_1 in enumerate(COMPANY_LIST):

        # when it connects with something else
        # continue
        if int(data_1[12]) != -1:
            continue

        [name_ko, name_en] = PREPROCESSING(iter_1, COMPANY_LIST)

        translation_name = ""

        # DEBUG:
        #print(translation_name)

        # iterate 0 ~ (iter_1)-1
        for iter_2 in range(iter_1+1, len(COMPANY_LIST)):
            # if name is same
            if int(COMPANY_LIST[iter_2][12]) != 0 and name_same_check(name_ko, name_en, translation_name, iter_2, COMPANY_LIST):
                #if set([COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]]) in CORRECT_DATA:
                #    COMPANY_LIST = merge(iter_1, iter_2, COMPANY_LIST)
                #elif set([COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]]) in INCORRECT_DATA:
                #    pass
                if validation_test(iter_1, iter_2, COMPANY_LIST):
                    # COMPANY_LIST = merge(iter_1, iter_2, COMPANY_LIST)
                    with open("correct_data_backup","a") as file:
                        file.write("{0}\t{1}\n".format(COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]))
                else:
                    with open("name_same_but_different","a") as file:
                        file.write("{0}\t{1}\n".format(COMPANY_LIST[iter_1][0], COMPANY_LIST[iter_2][0]))

        # if it is not changed
        if int(COMPANY_LIST[iter_1][12]) == -1:
            COMPANY_LIST[iter_1][12] = int(COMPANY_LIST[iter_1][0])

        # write_file
        write_file(FILE_NAME, COMPANY_LIST)

        # DEBUG:
        # print(str(COMPANY_LIST[iter_1][3]))
        # sys.stdout.flush()
