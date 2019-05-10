# -*- coding:utf-8 -*-
'''
    2개의 회사가 진짜로 동일한 회사인지 프로그래머가 확인하는 과정이다.
'''

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

# delete unnecessary parts from URL
def URL_PREPROCESSING(_URL):
    # url delimiters
    url_delimiters = ["https://", "http://", "www."]

    URL = _URL.strip().lower()

    for delimiter in url_delimiters:
        URL = URL.replace(delimiter,"")

    URL = URL.split(".")[0]

    return URL

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

    print("<{3}, {4}, {5}> and <{0}, {1}, {2}>".format(COMPANY_LIST[iterator2][0],COMPANY_LIST[iterator2][1],COMPANY_LIST[iterator2][2],\
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


# 2개가 동일한 회사인지 판단한다.
def validation_test(iterator1, iterator2, COMPANY_LIST):

    # URL'S are not empty
    if COMPANY_LIST[iterator1][4] and COMPANY_LIST[iterator2][4]:
        iter1_URL = URL_PREPROCESSING(COMPANY_LIST[iterator1][4])
        iter2_URL = URL_PREPROCESSING(COMPANY_LIST[iterator2][4])

        if iter1_URL == iter2_URL:
            return True

    # 사용자가 2개의 회사가 진짜 동일한지 확인하는 과정
    if User_Company_Validation(iterator1, iterator2, COMPANY_LIST):
        return True

    return False
