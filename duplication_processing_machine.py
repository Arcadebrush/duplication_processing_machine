# duplication_processing_machine ver 0.1
# 2018-11-28

# Import
import io, sys
import requests

# Koren output
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')


# company table/LIST classification
# is_user_request (0 : created by 기업생성 , 1 : created by 경력/프로젝트)
# member_count : members signed up company page
# homepage_url : company homepage url
# generated_user : user generated company
# merge_to : company should merge to "id"
COMPANY_TABLE = [ "id", "is_user_request", "member_count", "name_ko", "name_en", "url", "homepage_url", "generated_user", "merge_to"]
COMPANY_LIST = []

# school table/LIST classification
# name_other : english name
# permalink : rocketpunch link
# hompage : school homepage
# count : rocketpunch users in school
# verify_domain : email verification domain
SCHOOL_TABLE = ["id","name", "name_other", "permalink", "homepage", "count", "verify_domain"]
SCHOOL_LIST = []

# delete_company
# company_name should deleted
# deleted_name = []

# append new data
# company_name_out = open("company_name", "a", encoding="utf-8")
# additional_name_out = open("additional_name", "a", encoding="utf-8")
output_data = open("test-data-out_03","w", encoding="utf-8")

# Delimiters
# prefix and suffix
# delete delimiters in company/school name
Delimiters = ["(주)", "(사)", "(유)", "(재)", "㈜", "@", "#", "주)", "주식회사", "*", "사단법인", "-",
"inc.", "co.", "ltd.", " "]


# heapify
def heapify(arr, i, heap_size):
    smallest = i # Initialize smallest as root
    l = 2 * i + 1   # left = 2*i + 1
    r = 2 * i + 2  # right = 2*i + 2

    # See if left child of root exists and it's member_count
    # smaller than root
    if l < heap_size and int(arr[i][2]) > int(arr[l][2]):
        smallest = l

    # if the member_count is same, the more characters in company_name has priority
    if l < heap_size and int(arr[i][2]) == int(arr[l][2]):
        if len(arr[i][3] + arr[i][4]) > len(arr[l][3] + arr[l][4]):
            smallest = l

    # See if right child of root exists and it's member_count
    # smaller than root
    if r < heap_size and int(arr[smallest][2]) > int(arr[r][2]):
        smallest = r

    # if the member_count is same, the more characters in company_name has priority
    if r < heap_size and int(arr[smallest][2]) == int(arr[r][2]):
        if len(arr[smallest][3] + arr[smallest][4]) > len(arr[r][3] + arr[r][4]):
            smallest = r

    # Change root, if needed
    if smallest != i:
        arr[i],arr[smallest] = arr[smallest],arr[i] # swap

        # Heapify the root.
        heapify(arr, smallest, heap_size)

# heapsort
def heapSort(arr):
    size = len(arr)

    # Build a small heap
    for i in range(size, -1, -1):
        heapify(arr, i, size)

    # One by one extract elements
    for i in range(size-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i] # swap
        heapify(arr, 0, i)

    return arr

# print version informaion of this machine
def print_version_information():
    print("Duplication_processing_machine ver 0.1\n")

# loading data
def data_loading(__filename__):

    global COMPANY_LIST
    #output = open("company_sorted","a", encoding="utf-8")

    try :
        with open(__filename__, 'r', encoding="utf-8") as datafile:

            for line in datafile.readlines():
                line = line.replace("\n","").split('\t')

                # push back
                COMPANY_LIST.append(line)

            # do heap_sort
            # ascending order of memeber_count
            COMPANY_LIST = heapSort(COMPANY_LIST)

        print("loading " + str(__filename__) + " data is done successfully!")

    except:
        print("Fail to load " + str(__filename__) + " data!")

# print alert when those are same
def print_same_alert(iter1, iter2):
    print("\n<" + COMPANY_LIST[iter1][3] + ", " + COMPANY_LIST[iter1][4] + "> is same as " +
     "<" + COMPANY_LIST[iter2][3] + ", " + COMPANY_LIST[iter2][4] + "> and merged together")

# connect_company
# connect company if they have different merge_id
def connect_company(iter1, iter2):
    max_member_count = 0 # should merge to company has maximum member count

    # find merge_to company
    for iter in range(len(COMPANY_LIST)):
        if (COMPANY_LIST[iter][8] == COMPANY_LIST[iter1][8]) or (COMPANY_LIST[iter][8] == COMPANY_LIST[iter2][8]):
            if COMPANY_LIST[iter][2] > max_member_count:
                max_member_count = COMPANY_LIST[iter][2]
                merge_to_id = COMPANY_LIST[iter][8]
                id = iter

    # connect
    for iter in range(len(COMPANY_LIST)):
        if (COMPANY_LIST[iter][8] == COMPANY_LIST[iter1][8]) or (COMPANY_LIST[iter][8] == COMPANY_LIST[iter2][8]):
            print("\n<" + COMPANY_LIST[iter][3] + ", " + COMPANY_LIST[iter][4] + "> is connected with " +
             "<" + COMPANY_LIST[id][3] + ", " + COMPANY_LIST[id][4] + ">")
            COMPANY_LIST[iter][8] = merge_to_id


# is_same
# compare if COMPANY_LIST[iter1] is same COMPANY_LIST[iter2]
# compare COMPANY_LIST[iter1] to COMPANY_LIST[iter2]
def is_same(iter1, iter2):

    [name_ko_iter1, name_en_iter1] = PREPROCESSING(iter1)
    [name_ko_iter2, name_en_iter2] = PREPROCESSING(iter2)

    # if same
    if (name_ko_iter1 != "") and ((name_ko_iter1 == name_ko_iter2) or (name_ko_iter1 == name_en_iter2)):

        # have to merge it with
        # when it is alreay same with something
        if len(COMPANY_LIST[iter1]) > 8:
            # when they are not connected
            if COMPANY_LIST[iter1][8] != COMPANY_LIST[iter2][8]:
                connect_company(iter1, iter2)
            return True
        # else
        else:
            # add "merge_to" of iter2
            print_same_alert(iter1, iter2)
            COMPANY_LIST[iter1].append(COMPANY_LIST[iter2][8])
            return True

    elif (name_en_iter1 != "") and ((name_en_iter1 == name_ko_iter2) or (name_en_iter1 == name_en_iter2)):

        # have to merge it with
        # when it is alreay same with something
        if len(COMPANY_LIST[iter1]) > 8:
            # when they are not connected
            if COMPANY_LIST[iter1][8] != COMPANY_LIST[iter2][8]:
                connect_company(iter1, iter2)
            return True
        # else
        else:
            # add "merge_to" of iter2
            print_same_alert(iter1, iter2)
            COMPANY_LIST[iter1].append(COMPANY_LIST[iter2][8])
            return True
    # not same
    return False

# similar_test
# user input
# user tests if iter1 and iter2 are really similar (y/n)
def similar_test(iter1, iter2):
    # it doesn't have merge_to value yet
    print("\n<" + COMPANY_LIST[iter1][3] + ", " + COMPANY_LIST[iter1][4] + "> is similar to " +
     "<" + COMPANY_LIST[iter2][3] + ", " + COMPANY_LIST[iter2][4] + ">")
    yn = input("Merge them together? <y/n>\n")
    yn = yn.strip()

    if yn == "y" or yn == "Y":
        # have to merge it with
        # when it is alreay same/similar with something
        if len(COMPANY_LIST[iter1]) > 8:
            # do something
            return True

        # else
        else:
            # add "merge_to" of iter2
            COMPANY_LIST[iter1].append(COMPANY_LIST[iter2][8])
            return True

    else:
        return False

# compare_name
# compare either name_1 includes name_2 or vice versa
def compare_name(name_1, name_2):

    # if either is "", can't compare
    if len(name_1) == 0 or len(name_2) == 0:
        return False

    # set minimum_length
    minimum_length = (len(name_1) if len(name_1) < len(name_2) else len(name_2))

    # iterate index 0 to min_length-1
    for iterator in range(minimum_length):
        # compare character by character
        if name_1[iterator] != name_2[iterator]:
            return False

    return True

# is_similar
# check company name of iter1 and company name of iter2 are similar
# if name of iter1 includes name of iter2,
# those are similar companies, vice versa
# if they are similar merge all data to company that has more member_count
def is_similar(iter1, iter2):

    # preprocessing data
    [name_ko_iter1, name_en_iter1] = PREPROCESSING(iter1)
    [name_ko_iter2, name_en_iter2] = PREPROCESSING(iter2)

    # compare name_ko_iter1 to name_iter2
    if compare_name(name_ko_iter1, name_ko_iter2):
        return similar_test(iter1, iter2)
    elif compare_name(name_ko_iter1, name_en_iter2):
        return similar_test(iter1, iter2)

    # compare name_en_iter1 to name_iter2
    if compare_name(name_en_iter1, name_ko_iter2):
        return similar_test(iter1, iter2)
    elif compare_name(name_en_iter1, name_en_iter2):
        return similar_test(iter1, iter2)

    return False

# preprocessing
# delete prefix and suffix(Delimiters)
# for COMPANY_LIST[iter]
def PREPROCESSING(iter):

    name_ko = COMPANY_LIST[iter][3] # Company Korean name
    name_en = COMPANY_LIST[iter][4] # Company English name

    name_ko = name_ko.strip().lower()
    name_en = name_en.strip().lower()

    for delimiter in Delimiters:
        if delimiter in name_ko:
            name_ko = name_ko.replace(delimiter, "")
        if delimiter in name_en:
            name_en = name_en.replace(delimiter, "")

    return [name_ko, name_en]

# data_processing
# see algorithm at (https://github.com/Arcadebrush/duplication_processing_machine)
def data_processing():

    # time complexity O(n^2)
    for iter1 in range(len(COMPANY_LIST)):

        # variable to check if machine finds same/similar data
        done = False

        # check if company with same name exists in COMPANY_LIST
        # compare COMPANY_LIST[iter1] with COMPANY_LIST[0 ~ (iter1-1)]
        # check same data first
        for iter2 in range(0, iter1):

            # when page exists
            if COMPANY_LIST[iter2][8] != 0:

                done = is_same(iter1, iter2)

                # if iter1 is same as iter2
                if done :
                    break

        # if it doesn't have same data
        # check similar data
        if done is False:

            # check if company with similar name exists in COMPANY_LIST
            # compare COMPANY_LIST[iter1] with COMPANY_LIST[0 ~ (iter1-1)]
            for iter2 in range(0, iter1):

                # when page exists
                if COMPANY_LIST[iter2][8] != 0:

                    done = is_similar(iter1, iter2)

                    # if iter1 is similar to iter2
                    if done :
                        break

        # it is neither same nor similar
        if not done:
            COMPANY_LIST[iter1].append(COMPANY_LIST[iter1][0])

# post_processing
# if companies have same name
# but have different merge_to id
# connect them together
def post_processing():

    for iter1 in range(len(COMPANY_LIST)):

        # variable to check if machine finds same data
        done = False

        # check if company with same name exists in COMPANY_LIST
        # compare COMPANY_LIST[iter1] with COMPANY_LIST[iter1 + 1 ~ end]
        # check same data first
        for iter2 in range(iter1 + 1, len(COMPANY_LIST)):

            # when page exists
            if COMPANY_LIST[iter2][8] != 0:

                done = is_same(iter1, iter2)

                # if iter1 is same as iter2
                if done :
                    break


# main
if __name__ == "__main__":
    # 2 types of data(company, school)
    # each data is seperated with "tab"
    data_category = ["company", "school"]

    # duplication_processing_machine ver 0.1
    print_version_information()

    # data_loading
    print("------------ loading data ---------------")
    data_loading("test-data")
    #data_loading(data_category[0])
    #data_loading(data_category[1], SCHOOL_TABLE ,SCHOOL_DIC)
    print("-----------------------------------------\n")
    # data_loading done

    # data_processing
    data_processing()
    # data_processing done

    # connect companies if they are not
    print("\n------------ connecting companies ---------------")
    post_processing()
    print("\n-------------------------------------------------\n")
    # connect companies done

    # output data
    for iter in range(len(COMPANY_LIST)):
        for line in COMPANY_LIST[iter]:
            output_data.write(str(line) + "\t")
        output_data.write("\n")
