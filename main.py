# duplication_test_machine_ver_0.1

# pip install --upgrade google-cloud-translate
import os, sys
from google.cloud import translate

# Instantiates a client
translate_client = translate.Client()


import weight
from preprocessing import PREPROCESSING
from name_same_check import name_same_check
from validation_test import validation_test, information, COMPANY_TAG_PAGE_TEST
from merge import merge


# write_file
def write_file(__filename__, COMPANY_LIST):
    file = open(__filename__, "w", encoding="utf-8")

    for iter in range(len(COMPANY_LIST)):
        for data in COMPANY_LIST[iter]:
            file.write(str(data) + "\t")

        file.write("\n")

    file.close()

# loading data
def data_loading(__filename__, COMPANY_LIST):
    with open(__filename__, 'r', encoding="utf-8") as datafile:

        iterator = 0

        for line in datafile.readlines():
            # avoid overlapping
            line = line.strip().split('\t')

            # push back
            COMPANY_LIST.append(line)

            # if line doesn't have weight yet
            if len(line) < 14:
                # DEBUG:
                # print(iterator)
                COMPANY_LIST[iterator].append(weight.Calculate_weight(line, iterator, COMPANY_LIST))

            # if line doesn't have connected_with yet
            # it means it is not checked_yet
            if len(line) < 15:
                COMPANY_LIST[iterator].append("-1")

            iterator += 1


    print("loading " + str(__filename__) + " data is done successfully!")

    # write_file
    write_file(__filename__, COMPANY_LIST)

    return COMPANY_LIST

# COMAPNY_DELETE_TEST
def COMPANY_DELETE_TEST(COMPANY_LIST, iter_1):

    if int(COMPANY_LIST[iter_1][2]) == 0 and (not COMPANY_LIST[iter_1][6]) and int(COMPANY_LIST[iter_1][13]) <= 2:
        permalink = COMPANY_LIST[iter_1][5].replace("https://www.rocketpunch.com/companies/", "")

        if COMPANY_TAG_PAGE_TEST("https://www.rocketpunch.com/tag/" + permalink):
            # pip install selenium
            from selenium import webdriver

            BASE_DIR = os.getcwd()

            # chromedriver
            driver = webdriver.Chrome(os.path.join(BASE_DIR, "chromedriver.exe"))

            # permalink_page for iterator_1
            driver.get(COMPANY_LIST[iter_1][5])

            yn = input("Delete? <y/n>\n")
            yn = yn.strip()

            driver.close()

            if yn == "y" or yn == "Y":
                return True

            else:
                return False


if __name__=="__main__":

    COMPANY_LIST = []

    # __filename__
    COMPANY_LIST = data_loading("company0.190108", COMPANY_LIST)

    # time_complexity O(N^2)
    for iter_1 in range(len(COMPANY_LIST)):

        if int(COMPANY_LIST[iter_1][14]) != -1:
            continue

        # Korean_name and English_name
        [name_ko, name_en] = PREPROCESSING(iter_1, COMPANY_LIST)

        # translated name

        result = translate_client.detect_language(name_ko)

        # only korean
        if result['language'] == "ko":

            target_lang = "en"

            translation = translate_client.translate(
                name_ko,
                target_language=target_lang)

            translation_name = translation['translatedText'].lower().replace(" ","")

        else:
            translation_name = ""

            # DEBUG:
            # print(translation_name)

        # COMAPNY_DELETE_TEST
        # it doesnt't have logo, 한 줄 소개, 기업 소개
        # member_count, old person, URL
        # USER_defines whether delete it
        if COMPANY_DELETE_TEST(COMPANY_LIST, iter_1):
            COMPANY_LIST[iter_1][14] = 0

            # write_file
            write_file("company0.190108", COMPANY_LIST)

            continue

        # iterate 0 ~ (iter_1)-1
        for iter_2 in range(iter_1):
            # if name is same
            if name_same_check(name_ko, name_en, translation_name, iter_2, COMPANY_LIST):
                if validation_test(iter_1, iter_2, COMPANY_LIST):
                    COMPANY_LIST = merge(iter_1, iter_2, COMPANY_LIST)
                    break

        # if it is not changed
        if int(COMPANY_LIST[iter_1][14]) == -1:
            COMPANY_LIST[iter_1][14] = int(COMPANY_LIST[iter_1][0])

        # write_file
        write_file("company0.190108", COMPANY_LIST)

        # DEBUG:
        # print(str(COMPANY_LIST[iter_1][3]))
        # sys.stdout.flush()
