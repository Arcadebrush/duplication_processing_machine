# PREPROCESSING
# delete delimiters from name_ko, name_en

# Delimiters
# unnecessary parts from name
Delimiters = ["(주)", "(사)", "(유)", "(재)", "㈜", "@", "#", "주)", "사)", "유)",
"재)","주식회사", "*", "사단법인", "-", "Co., Ltd.","Co., LTD",
"inc.", "co.", "ltd.", ".", "/", ",", " "]

# preprocessing
# delete prefix and suffix(Delimiters)
# for COMPANY_LIST[iterator]
def PREPROCESSING(iterator, COMPANY_LIST):

    name_ko = COMPANY_LIST[iterator][3] # Company Korean name
    name_en = COMPANY_LIST[iterator][4] # Company English name

    name_ko = name_ko.strip().lower()
    name_en = name_en.strip().lower()

    for delimiter in Delimiters:
        if delimiter in name_ko:
            name_ko = name_ko.replace(delimiter, "")
        if delimiter in name_en:
            name_en = name_en.replace(delimiter, "")

    return [name_ko, name_en]