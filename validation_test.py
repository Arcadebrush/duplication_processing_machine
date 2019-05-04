# -*- coding:utf-8 -*-
# validation_test

import os

# pip install selenium
from selenium import webdriver

desktop_agents = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

def random_headers():
    return {'User-Agent': random.choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}


# URL_PREPROCESSING
# delete unnecessary parts from URL
def URL_PREPROCESSING(_URL):
    # url delimiters
    url_delimiters = ["https://", "http://", "www."]

    URL = _URL.strip().lower()

    for delimiter in url_delimiters:
        URL = URL.replace(delimiter,"")

    URL = URL.split(".")[0]

    return URL

# information
# validate company has logo or 한 줄 소개, 기업 소개
def information(COMPANY_LIST_LINE):
    return (COMPANY_LIST_LINE[6]) or (COMPANY_LIST_LINE[7]) or (COMPANY_LIST_LINE[8]) or \
    (COMPANY_LIST_LINE[9]) or (COMPANY_LIST_LINE[10])

# User_Company_Validation
# User validates if company is really same
def User_Company_Validation(iterator1, iterator2, COMPANY_LIST):

    BASE_DIR = os.getcwd()

    # chromedriver
    driver = webdriver.Chrome(os.path.join(BASE_DIR, "chromedriver"))

    # permalink_page for iterator_1
    driver.get(COMPANY_LIST[iterator1][3])

    # second page for iterator_2
    driver.execute_script("window.open('about:blank', 'tab2');")
    driver.switch_to.window("tab2")
    driver.get(COMPANY_LIST[iterator2][3])

    print("<{0}, {1}, {2}> and <{3}, {4}, {5}>".format(COMPANY_LIST[iterator2][0],COMPANY_LIST[iterator2][1],COMPANY_LIST[iterator2][2],\
    COMPANY_LIST[iterator1][0],COMPANY_LIST[iterator1][1], COMPANY_LIST[iterator1][2]))
    yn = raw_input("Same? <y/n>\n")
    yn = yn.strip()

    # close driver
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.close()

    if yn == "y" or yn == "Y":
        return True

    else:
        return False

# COMPANY_TAG_PAGE_TEST
# www.rocketpunch.com/tag/[permalink]
# validate no person
def COMPANY_TAG_PAGE_TEST(tag_url):
    try:
        plain_txt = requests.get(tag_url, headers=random_headers())

        if plain_txt.status_code == 404:
            return False

        sleep(1)

        soup = BeautifulSoup(plain_txt.content, "html.parser")

        div = soup.find("div" , class_="eight wide object column")

        a = div.find("a").text

        number = int(a.replace("전/현재 구성원 ", ""))

        if number >= 1:
            return False

        else:
            return True

    except:
        return True


# validate 2 companies are same
def validation_test(iterator1, iterator2, COMPANY_LIST):

    # URL'S are not empty
    if COMPANY_LIST[iterator1][4] and COMPANY_LIST[iterator2][4]:
        iter1_URL = URL_PREPROCESSING(COMPANY_LIST[iterator1][4])
        iter2_URL = URL_PREPROCESSING(COMPANY_LIST[iterator2][4])

        if iter1_URL == iter2_URL:
            return True

    # User check
    # when both companies have enough information
    if information(COMPANY_LIST[iterator1]) and information(COMPANY_LIST[iterator2]):
        # User Check section
        if User_Company_Validation(iterator1, iterator2, COMPANY_LIST):
            return True

    else:
        # no logo, 한 줄 소개, 기업 소개
        if not information(COMPANY_LIST[iterator1]):
            # member_count == 0, no_URL
            if int(COMPANY_LIST[iterator1][5]) == 0 and (not COMPANY_LIST[iterator1][4]):
                permalink = COMPANY_LIST[iterator1][3].replace("https://www.rocketpunch.com/companies/", "")

                # no old member
                if COMPANY_TAG_PAGE_TEST("https://www.rocketpunch.com/tag/" + permalink):
                    return True

                # exist old member
                else:
                    return False

        # when current_member_exist
        if int(COMPANY_LIST[iterator1][5]) > 0 and int(COMPANY_LIST[iterator2][5]) > 0:
            # User Check section
            if User_Company_Validation(iterator1, iterator2, COMPANY_LIST):
                return True

    return False
