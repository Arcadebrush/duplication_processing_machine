# duplication_processing_machine ver 0.1
# made by JYH
# 2018-11-28

# Import
import io, sys


# Koren output
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# company table/dictionary classification
# is_user_request (0 : created by 기업생성 , 1 : created by 경력/프로젝트)
# member_count : members signed up company page
# homepage_url : company homepage url
# generated_user : user generated company
COMPANY_TABLE = [ "id", "is_user_request", "member_count", "name_ko", "name_en", "url", "homepage_url", "generated_user"]
COMPANY_DIC = {
    "id" : [],
    "is_user_request" : [],
    "member_count" : [],
    "name_ko" : [],
    "name_en" : [],
    "url" : [],
    "homepage_url" : [],
    "generated_user" : []
}

# school table/dictionary classification
# name_other : english name
# permalink : rocketpunch link
# hompage : school homepage
# count : rocketpunch users in school
# verify_domain : email verification domain
SCHOOL_TABLE = ["id","name", "name_other", "permalink", "homepage", "count", "verify_domain"]
SCHOOL_DIC = {
    "id" : [],
    "name" : [],
    "name_other" : [],
    "permalink" : [],
    "homepage" : [],
    "count" : [],
    "verify_domain" : []
}


# global variables

# company_name
# ex) 삼성전자, 로켓펀치, LG
company_name = []

# additional_name
# ex) 가전사업부, VE, 등
additional_name = []

# connected_compnay
# connected_company has same key valueullim
connected_company = []
last_key = 0

# append new data
company_name_out = open("company_name", "a", encoding="utf-8")
additional_name_out = open("additional_name", "a", encoding="utf-8")


# Delimiters
# prefix and suffix
# delete delimiters in company/school name
Delimiters = ["(주)", "(사)", "(유)", "(재)", "㈜", "@", "#", "주)", "주식회사", "*", "사단법인", "-",
"inc.", "co.", "ltd.", " "]


# print version informaion of this machine
def print_version_information():
    print("Duplication_processing_machine ver 0.1\n")


# loading data
def data_loading(__filename__, TABLE, DICTIONARY):
    try :
        with open(__filename__, 'r', encoding="utf-8") as datafile:
            for line in datafile.readlines():
                line = line.rstrip().split('\t')

                for data, iterator in zip(line, range(len(TABLE))):
                    # push_back
                    DICTIONARY[TABLE[iterator]].insert(len(DICTIONARY[TABLE[iterator]]), data)

        print("loading " + str(__filename__) + " data is done successfully!")

    except:
        print("Fail to load " + str(__filename__) + "data!")

# data_processing
# 2 parts
# PREPROCESSING
# PROCESSING
def data_processing(DICTIONARY):

    for iterator in range(len(DICTIONARY["id"])):
        # preprocessing data
        [name_ko, name_en, o_name_ko, o_name_en] = PREPROCESSING(DICTIONARY["name_ko"][iterator], DICTIONARY["name_en"][iterator])

        # proceesing data
        PROCESSING(name_ko, name_en, o_name_ko, o_name_en)

        company_name_out.flush()
        additional_name_out.flush()

# loading machine data
def machine_data_loading():

    global company_name
    global connected_company
    global additional_name
    global last_key

    try :
        company = open("company_name", "r", encoding="utf-8")
        additional = open("additional_name", "r", encoding="utf-8")

        for line1 in company.readlines():
            line1 = line1.strip().split('\t')
            company_name.append(line1[0])
            connected_company.append(line1[1])

            if int(line1[1]) > last_key:
                last_key = int(line1[1])

        print("loading company_name data is done successfully!")
        print("loading additional_name data is done successfully!")

        for line1 in additional.readlines():
            additional_name.append(line1.strip())

        print("loading connected_company data is done successfully!")

        company.close()
        additional.close()

    except:
        print("Fail to load machine data!")
        company.close()
        additional.close()

# verification
# user input need
def verification_test(name_ko, max_name):
    while True:
        yn = input("company_name : " + str(max_name) + "\t additional_name : " + str(name_ko.replace(max_name,"")) + "  (y/n)\n")

        yn = yn.strip()

        if yn == "y":
            additional_name.append(name_ko.replace(max_name,""))
            return True
        elif yn == "n":
            return False


# is_same
# return connected_key if input A is in the company_name
def is_same(name_ko, name_en):

    ko_key = -1
    en_key = -1

    for idx in range(len(company_name)):
        if name_ko == company_name[idx]:
            ko_key = connected_company[idx]
        if name_en == company_name[idx]:
            en_key = connected_company[idx]

    # both are in the list
    if ko_key != -1 and en_key != -1:
        # error
        if ko_key != en_key:
            print("Error! : " + str(name_ko) + "\t" + str(name_en) + " are not connected!")
        else:
            return True
    # at least one is in the list
    elif ko_key != -1:
        # input new company in the list
        if name_en != "":
            company_name_out.write(str(name_en) + "\t" + str(ko_key) + "\n")
            company_name.append(str(name_en))
            connected_company.append(ko_key)
            print(str(name_en) + " is new data and conneted with " + str(name_ko))
        return True
    elif en_key != -1:
        # input new company in the list
        if name_ko != "":
            company_name_out.write(str(name_ko) + "\t" + str(en_key) + "\n")
            company_name.append(str(name_ko))
            connected_company.append(en_key)
            print(str(name_ko) + " is new data and conneted with " + str(name_en))
        return True
    # neither is in the list
    else:
        return False

# is_similar
#
#
def is_similar(name_ko, name_en):

    # find max_common_length
    max_length = 0
    max_name = ""

    for c_name in company_name:
        # when company_name is same:
        if c_name in name_ko:
            if len(c_name) > max_length:
                max_length = len(c_name)
                max_name = c_name

    # common part exist
    if max_length > 0:
        for a_name in additional_name:
            # when additional_name is same:
            if a_name == name_ko.replace(max_name,""):
                # implement name_en here
                return True

        # verification_test
        if verification_test(name_ko,max_name) is False:
            return False
    else:
        # company_add
        return False

# add company
# user section
# implement en name
#
def add_company(o_name_ko, o_name_en):

    global last_key

    if o_name_ko != "" or o_name_en != "":

        print("\nPlease seperate <" + str(o_name_ko) + ", " + str(o_name_en) + ">\n")

        cn = input("company_name : ")
        cn = cn.strip()

        if cn != "/a":
            an = input("addtion name : ")
            an = an.strip()

        if cn != "":
            if cn == "/a":
                last_key += 1
                company_name.append(o_name_ko)
                connected_company.append(last_key)
                company_name_out.write(str(o_name_ko) + "\t" + str(last_key) + "\n")
            else:
                last_key += 1
                company_name.append(cn)
                connected_company.append(last_key)
                company_name_out.write(str(cn) + "\t" + str(last_key) + "\n")

        if cn != "/a" and an != "":
            additional_name.append(an)
            additional_name_out.write(str(an) + "\n")


# preprocessing
# delete prefix and suffix(Delimiters)
def PREPROCESSING(name_ko, name_en):

    # original data
    o_name_ko = name_ko
    o_name_en = name_en

    for delimiter in Delimiters:
        if delimiter in name_ko.strip().lower():
            name_ko = name_ko.strip().lower().replace(delimiter, "")
        if delimiter in name_en.strip().lower():
            name_en = name_en.strip().lower().replace(delimiter, "")

    return [name_ko, name_en, o_name_ko, o_name_en]

# PROCESSING
#
# see algorithm at Reference below
# Reference (https://docs.google.com/document/d/1rjr01xp-GpOVCBc01_yc2SAy3ClSEaV9jlMgx8lNefc/edit)
def PROCESSING(name_ko, name_en, o_name_ko, o_name_en):

    # is not same
    if is_same(name_ko, name_en) is False:

        # is not similar
        if is_similar(name_ko, name_en) is False:
            # add_company
            add_company(o_name_ko, o_name_en)



# main
if __name__ == "__main__":
    # 2 types of data(company, school)
    # each data is seperated "tab"
    data_category = ["company", "school"]

    # duplication_processing_machine ver 0.1
    # made by JYH
    print_version_information()

    # data_loading
    print("------------ loading data ---------------")
    data_loading(data_category[0], COMPANY_TABLE ,COMPANY_DIC)
    #data_loading(data_category[1], SCHOOL_TABLE ,SCHOOL_DIC)
    print("-----------------------------------------\n")
    # data_loading done

    # loading duplication information
    print("------------ loading machine data -------")
    machine_data_loading()
    print("-----------------------------------------\n")
    # loading duplication information done

    # data_processing
    data_processing(COMPANY_DIC)
