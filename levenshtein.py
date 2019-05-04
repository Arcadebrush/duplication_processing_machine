# -*- coding:utf-8 -*-
# levenshtein.py
'''
    Calculate levenshtein distance between 2 words
'''

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]

if __name__ == "__main__":
    DATA = []
    with open("samsung","r") as file:
        DATA = file.read().splitlines()
    for iter, data in enumerate(DATA):
        DATA[iter] = data.split("\t")

    for iter_1, dt1 in enumerate(DATA):
        name_ko = dt1[1]
        name_en = dt1[2]

        name_ko = unicode(name_ko)

        for iter_2 in range(iter_1):
            name_ko_com = DATA[iter_2][1]
            name_en_com = DATA[iter_2][2]

            name_ko_com = unicode(name_ko_com)

            print("<{0}, {1} = {2}>".format(name_ko,name_ko_com, levenshtein(name_ko, name_ko_com)))
