# duplication_processing_machine ver 0.1
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

# find_key
# return key number
def find_key(name):

    name = name.strip().lower()

    for idx in range(len(company_name)):
        if name == company_name[idx]:
            return connected_company[idx]

    # not exist
    return -1

# validation_test
# check if machine seperate data well
# user input
def validation_test(name, max_name):
    while True:
        # ex
        # <samsung electronics> is already in the list
        # <samsung electronic> is input
        if len(name) < len(max_name):
            print("\n" + str(name) + " is similar to " + str(max_name))
            yn = input("merge " + str(name) + " to " + str(max_name) + " ? (y/n)\n")
            yn = yn.strip()

            if yn == "y":
                print(str(name) + " is merged to " + str(max_name))
                # list input
                company_name.append(name)
                connected_company.append(find_key(max_name))

                # database input
                company_name_out.write(str(name) + "\t" + str(find_key(max_name)) + "\n")
                return True
            elif yn == "n":
                return False

        # ex
        # <samsung electronic> is already in the list
        # <samsung electronics> is input
        else:
            print("\n" + str(name) + " is similar to " + str(max_name))
            yn = input("merge " + str(name) + " to " + str(max_name) + " ? (y/n)\n")
            yn = yn.strip()
            if yn == "y":
                print(str(name) + " is merged to " + str(max_name))
                # list input
                company_name.append(name)
                connected_company.append(find_key(max_name))

                # database input
                company_name_out.write(str(name) + "\t" + str(find_key(max_name)) + "\n")
                return True

            else :
                print("\nseperate " + str(name))
                yn = input("company_name : " + str(max_name) + "\t additional_name : " + str(name.replace(max_name,"")) + "  (y/n)\n")

                yn = yn.strip()

                if yn == "y":
                    print(str(name.replace(max_name,"")) + " is added to the additional_name")
                    # list input
                    additional_name.append(name.replace(max_name,""))

                    # database input
                    additional_name_out.write(str(name.replace(max_name,"")) + "\n")
                    return True
                elif yn == "n":
                    return False

# merge_company
# merge same companies has different key value
def merge_company(ko_key, en_key):

    # merge to lower key value
    lower_key = (ko_key if ko_key < en_key else en_key)
    higher_key = (ko_key if ko_key > en_key else en_key)

    for idx in range(len(company_name)):
        if connected_company[idx] == higher_key:
            connected_company[idx] = lower_key

    print("Companies are merged!")

# is_same
# return True if the company A is already in the list
def is_same(name_ko, name_en, o_name_ko, o_name_en):

    ko_key = -1
    en_key = -1

    ko_key = find_key(name_ko)
    en_key = find_key(name_en)

    # both are in the list
    if ko_key != -1 and en_key != -1:
        # error
        if ko_key != en_key:
            merge_company(ko_key, en_key)
            return True
        else:
            return True

    # Korean name is in the list
    elif ko_key != -1:
        # input English name into the list
        if name_en != "":
            # output to database
            company_name_out.write(str(name_en) + "\t" + str(ko_key) + "\n")

            # output to list
            company_name.append(str(name_en))
            connected_company.append(ko_key)

            print("\n" + str(o_name_en) + " is a new data and conneted with " + str(o_name_ko))
        return True

    # English name is in the list
    elif en_key != -1:
        # input Korean name in the list
        if name_ko != "":
            # output to database
            company_name_out.write(str(name_ko) + "\t" + str(en_key) + "\n")

            # output to list
            company_name.append(str(name_ko))
            connected_company.append(en_key)
            print("\n" + str(o_name_ko) + " is a new data and conneted with " + str(o_name_en))
        return True

    # neither is in the list
    else:
        return False

# is_similar
# find the longest common string
# seperate name into 2 parts (longest common string, additional string)
# check this seperation is valid
def is_similar(name):

    if name == "":
        return False

    max_length = 0
    max_name = ""

    for c_name in company_name:
        # find the longest common string
        if c_name in name:
            if len(c_name) > max_length:
                max_length = len(c_name)
                max_name = c_name

        # in case name is in company_name
        if name in c_name:
            max_name = c_name
            if validation_test(name, max_name) is False:
                # add company
                return False

            else:
                return max_name

    # common string exist
    if max_length > 0:
        for a_name in additional_name:
            # when additional_name is same:
            if a_name == name.replace(max_name,""):
                print(str(name.replace(max_name,"")) + " is already in additional_name")
                # return company_name
                return max_name

        # validation_test fail
        if validation_test(name, max_name) is False:
            # add company
            return False
        # else
        else :
            # return company_name
            return max_name

    # else
    else:
        # add_company
        return False

# add company
# add company with name
# assign same conneted key number with connected_company
# user input
def add_company(name, connected_company_name, o_name):

    # last_key of connected_company key
    global last_key

    if name != "":

        print("\nPlease seperate <" + str(o_name) + ">\n")

        # user input
        cn = input("company_name : ")
        cn = cn.strip()
        an = ""

        if cn != "/a":
            an = input("additional_name : ")
            an = an.strip()
            print("deleted_part : " + str(o_name.replace(cn,"").replace(an,"")))

        # in case user input wrongly
        [cn, an, o_cn, o_an] = PREPROCESSING(cn,an)

        # if additional_name exist
        if cn != "/a" and an != "":

            # additional_name duplication check
            a_check  = False

            for a_name in additional_name:
                if a_name == an:
                    a_check = True
                    break

            if a_check == False:
                # list input
                additional_name.append(an)
                # database input
                additional_name_out.write(str(an) + "\n")

                print("\n" + str(an) + " is added in additional_name")

            else:
                print("\n" + str(an) + " is already in the additional_name")

        if cn != "":
            # all
            if cn == "/a":
                # connected_company exist
                if connected_company_name != "":
                    key = find_key(connected_company_name)

                    # list input
                    company_name.append(name)
                    connected_company.append(key)

                    # database input
                    company_name_out.write(str(name) + "\t" + str(key) + "\n")

                    print("\n" + str(name) + " is added in company_name and conneted with " + str(connected_company_name))

                # else
                else:
                    # duplication test_data
                    # check new korean name is already in the list
                    key = find_key(name)

                    if key == -1:
                        last_key += 1
                        # list input
                        company_name.append(name)
                        connected_company.append(last_key)

                        # database input
                        company_name_out.write(str(name) + "\t" + str(last_key) + "\n")

                        print("\n" + str(name) + " is added in company_name")

                    else :
                        print("\n" + str(name) + " is already in company_name")

                return name

            # not all
            else:
                # connected_company exist
                if connected_company_name != "":
                    key = find_key(connected_company_name)

                    # list input
                    company_name.append(cn)
                    connected_company.append(key)

                    # database input
                    company_name_out.write(str(cn) + "\t" + str(key) + "\n")

                    print("\n" + str(cn) + " is added in company_name and conneted with " + str(connected_company_name))
                # else
                else:
                    # duplication test_data
                    # check new korean name is already in the list
                    key = find_key(cn)

                    if key == -1 :
                        last_key += 1
                        # list input
                        company_name.append(cn)
                        connected_company.append(last_key)

                        # database input
                        company_name_out.write(str(cn) + "\t" + str(last_key) + "\n")

                        print("\n" + str(cn) + " is added in company_name")

                    else:
                        print("\n" + str(cn) + " is already in company_name")

                return cn

    else :
        return ""

# preprocessing
# delete prefix and suffix(Delimiters)
def PREPROCESSING(name_ko, name_en):

    # original data
    o_name_ko = name_ko
    o_name_en = name_en

    name_ko = name_ko.strip().lower()
    name_en = name_en.strip().lower()

    for delimiter in Delimiters:
        if delimiter in name_ko:
            name_ko = name_ko.replace(delimiter, "")
        if delimiter in name_en:
            name_en = name_en.replace(delimiter, "")

    return [name_ko, name_en, o_name_ko, o_name_en]

# PROCESSING
#
# see algorithm at Reference below
# Reference (https://docs.google.com/document/d/1rjr01xp-GpOVCBc01_yc2SAy3ClSEaV9jlMgx8lNefc/edit)
def PROCESSING(name_ko, name_en, o_name_ko, o_name_en):

    # is not same
    if is_same(name_ko, name_en, o_name_ko, o_name_en) is False:

        ko_similar = is_similar(name_ko)
        en_similar = is_similar(name_en)

        # both are in the list
        if ko_similar is not False and en_similar is not False:
            pass

        # only name_ko is in the list
        elif ko_similar is not False:
            # ko_similar is company_name of name_ko
            add_company(name_en, ko_similar, o_name_en)

        # only name_en is in the list
        elif en_similar is not False:
            # en_similar is company_name of name_en
            add_company(name_ko, en_similar, o_name_ko)

        # bot are not in the list
        else:
            # return of add_company is company_name
            add_company(name_en, add_company(name_ko, "", o_name_ko), o_name_en)

# PRINT_CONNECTION
# print connected list companies
def PRINT_CONNECTION():
    yn = input("PRINT_CONNECTION? : ")

    if yn == "y":
        print("-------------------------------------")

        set_connected_company = set(connected_company)

        for key in set_connected_company:
            for idx in range(len(company_name)):
                if key == connected_company[idx]:
                    sys.stdout.write(company_name[idx] + ", ")
            print()

        print("-------------------------------------")

        return

    else :
        return


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

        # for debugging
        # PRINT_CONNECTION()

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
    data_loading("test_data/samsung", COMPANY_TABLE ,COMPANY_DIC)
    #data_loading(data_category[0], COMPANY_TABLE ,COMPANY_DIC)
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
