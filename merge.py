# merge

# compare weight of company
def merge(iter_1, iter_2, COMPANY_LIST):

    # when delete
    if int(COMPANY_LIST[iter_2][14]) == 0:
        COMPANY_LIST[iter_1][14] = 0
        return COMPANY_LIST

    # DEBUG:
    # print(COMPANY_LIST[iter_2][14])

    # find connected_with company
    for iter in range(len(COMPANY_LIST)):
        if int(COMPANY_LIST[iter_2][14]) == int(COMPANY_LIST[iter][0]):
            connected_with_iter = iter
            connected_with_id = int(COMPANY_LIST[iter][0])
            break

    # compare weight

    # if completeness is different
    if int(COMPANY_LIST[iter_1][13])/4 != int(COMPANY_LIST[connected_with_iter][13])/4:

        if int(COMPANY_LIST[connected_with_iter][13]) > int(COMPANY_LIST[iter_1][13]):
            COMPANY_LIST[iter_1][14] = int(COMPANY_LIST[iter_2][14])

            return COMPANY_LIST

        else:
            # change connected_with
            for iter in range(len(COMPANY_LIST)):
                if int(COMPANY_LIST[iter][14]) == int(connected_with_id):
                    COMPANY_LIST[iter][14] = int(COMPANY_LIST[iter_1][0])

            COMPANY_LIST[iter_1][14] = int(COMPANY_LIST[iter_1][0])

            return COMPANY_LIST

    # compare using member_count
    else :

        # compare (weight + member_count)
        if int(COMPANY_LIST[connected_with_iter][13]) + int(COMPANY_LIST[connected_with_iter][2]) \
        >= int(COMPANY_LIST[iter_1][13]) + int(COMPANY_LIST[iter_1][2]):
            COMPANY_LIST[iter_1][14] = int(COMPANY_LIST[iter_2][14])

            return COMPANY_LIST

        else:
            # change connected_with
            for iter in range(len(COMPANY_LIST)):
                if int(COMPANY_LIST[iter][14]) == int(connected_with_id):
                    COMPANY_LIST[iter][14] = int(COMPANY_LIST[iter_1][0])

            COMPANY_LIST[iter_1][14] = int(COMPANY_LIST[iter_1][0])

            return COMPANY_LIST
