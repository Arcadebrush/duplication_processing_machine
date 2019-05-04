# -*- coding:utf-8 -*-
# merge

# compare weight of company
def merge(iter_1, iter_2, COMPANY_LIST):

    # when delete
    if int(COMPANY_LIST[iter_2][12]) == 0:
        COMPANY_LIST[iter_1][12] = 0
        return COMPANY_LIST

    # DEBUG:
    # print(COMPANY_LIST[iter_2][12])

    connected_with_iter = iter_2
    connected_with_id = int(COMPANY_LIST[iter_2][0])

    if int(COMPANY_LIST[iter_2][12]) == -1:
        COMPANY_LIST[iter_2][12] = int(COMPANY_LIST[iter_2][0])

    # find connected_with company
    for iter in range(len(COMPANY_LIST)):
        if int(COMPANY_LIST[iter_2][12]) == int(COMPANY_LIST[iter][0]):
            connected_with_iter = iter
            connected_with_id = int(COMPANY_LIST[iter][0])
            break

    # compare weight

    # if completeness is different
    if int(COMPANY_LIST[iter_1][11])/4 != int(COMPANY_LIST[connected_with_iter][11])/4:

        if int(COMPANY_LIST[connected_with_iter][11]) > int(COMPANY_LIST[iter_1][11]):
            COMPANY_LIST[iter_1][12] = int(COMPANY_LIST[iter_2][12])

            return COMPANY_LIST

        else:
            # change connected_with
            for iter in range(len(COMPANY_LIST)):
                if int(COMPANY_LIST[iter][12]) == int(connected_with_id):
                    COMPANY_LIST[iter][12] = int(COMPANY_LIST[iter_1][0])

            COMPANY_LIST[iter_1][12] = int(COMPANY_LIST[iter_1][0])

            return COMPANY_LIST

    # compare using member_count
    else :

        # compare (weight + member_count)
        if int(COMPANY_LIST[connected_with_iter][11]) + int(COMPANY_LIST[connected_with_iter][5]) \
        >= int(COMPANY_LIST[iter_1][11]) + int(COMPANY_LIST[iter_1][5]):
            COMPANY_LIST[iter_1][12] = int(COMPANY_LIST[iter_2][12])

            return COMPANY_LIST

        else:
            # change connected_with
            for iter in range(len(COMPANY_LIST)):
                if int(COMPANY_LIST[iter][12]) == int(connected_with_id):
                    COMPANY_LIST[iter][12] = int(COMPANY_LIST[iter_1][0])

            COMPANY_LIST[iter_1][12] = int(COMPANY_LIST[iter_1][0])

            return COMPANY_LIST
