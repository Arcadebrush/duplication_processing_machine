# -*- coding:utf-8 -*-
'''
    영문이 포함되어 있는 이름을 한글로 변경시키는 것
'''

#특정한 이름
trans_dictionary = {
    "naver" : "네이버",
    "samsung" : "삼성",
    "daum" : "다음",
    "kakao" : "카카오",
    "daumkakao" : "다음카카오",
    "kaist" : "카이스트",
    "카이스트" : "한국과학기술원",
    "skt" : "에스케이텔레콤"
}

word_dictionary = {
    "a" : "에이", "b" : "비", "c" : "씨", "d" : "디", "e" : "이", "f" : "에프", "g" : "지", "h" : "에이치", "i" : "아이",
    "j" : "제이", "k" : "케이", "l" : "엘", "n" : "엔", "m" : "엠", "o" : "오", "p" : "피","q" : "큐","r" : "알",
    "s" : "에스" ,"t" : "티","u" : "유","v" : "브이", "w" : "더블유", "x" : "엑스","y" : "와이", "z" : "지", "&" : "앤"
}


def translate(name_list):
    trans_list = []

    for name in name_list:
        # 예외 사항들
        for key in sorted(trans_dictionary.keys()):
            if key in name:
                name = name.replace(key, trans_dictionary[key])
                trans_list.append(name)

        # 로마자 - 한글 번역
        for key, value in word_dictionary.items():
            if key in name:
                name = name.replace(key, value)

        trans_list.append(name)

    return trans_list
