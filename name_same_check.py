# name_same_check
from google.cloud import translate
from preprocessing import PREPROCESSING

# Instantiates a client
translate_client = translate.Client()

# compare COMPANY_LIST[iterator1] and COMPANY_LIST[iterator2]
def name_same_check(name_ko, name_en, translation_name, iterator2, COMPANY_LIST):

    # preprocessing
    [iter2_ko_name, iter2_en_name] = PREPROCESSING(iterator2, COMPANY_LIST)

    # if it is korean
    result = translate_client.detect_language(iter2_ko_name)

    if result['language'] == "ko":

        target_lang = "en"

        translation = translate_client.translate(
            iter2_ko_name,
            target_language=target_lang)

        tr_name = translation['translatedText'].lower().replace(" ","")

    else:
        tr_name = ""

    # DEBUG:
    # print(iter2_ko_name)
    # print(name_ko)

    # completely same
    if name_ko:   # not empty
        if (name_ko == iter2_ko_name) or (name_ko == iter2_en_name):

            # DEBUG:
            # print("true")

            return True

    if name_en:   # not empty
        if (name_en == iter2_ko_name) or (name_en == iter2_en_name):
            return True

    if translation_name:   # not empty
        if (translation_name == iter2_ko_name) or (translation_name == iter2_en_name):
            return True

    if tr_name: # not empty
        if (tr_name == name_ko) or (tr_name == name_en) or (tr_name == translation_name):
            return True

    # inclusive same
    if name_ko and name_en:
        if (name_ko in iter2_ko_name) and (name_en in iter2_ko_name):
            return True

        if (name_ko in iter2_en_name) and (name_en in iter2_en_name):
            return True

    if iter2_ko_name and iter2_en_name:
        if (iter2_ko_name in name_ko) and (iter2_en_name in name_ko):
            return True

        if (iter2_ko_name in name_en) and (iter2_en_name in name_en):
            return True


    return False
