# -*- coding:utf-8 -*-
'''
    로켓펀치내 학교데이터 중복처리를 진행하는 파일
'''
import io, sys, os

# Delimiters
# unnecessary names
# delete delimiters in school name
Delimiters = [",", "+", ".", "’", "ㆍ", "/" ,"-", " ",'"']


# loading data
def data_loading(__filename__):

    global SCHOOL_LIST

    with open(__filename__, 'r') as datafile:

        for line in datafile.readlines():
            line = line.replace("\n","").split('\t')

            # push back
            SCHOOL_LIST.append(line)

    print("loading " + str(__filename__) + " data is done successfully!")

# delete_unnecessary
# delete_unnecessary parts in the name and url
def delete_unnecessary(LIST):

    # lower and strip
    name = LIST[1].strip().lower()
    name_other = LIST[2].strip().lower()

    # delete delimiter in the name and name_other
    for delimiter in Delimiters:
        # name
        if delimiter in name:
            name = name.replace(delimiter,"")

        # name_other
        if delimiter in name_other:
            name_other = name_other.replace(delimiter,"")


    return [name, name_other]

# other_case
def other_case(name, name_list):

    dic = {'대학교': [('대학교', '대')],
           '여자고등학교' : [('여자고등학교', '여고')],
           '여자중학교' : [('여자중학교', '여중')],
           '남자고등학교' : [('남자고등학교', '남고')],
           '남자중학교' : [('남자중학교', '남중')],
           '과학고등학교' : [('과학고등학교', '과고')],
           '외국어고등학교' : [('외국어고등학교', '외고')],
           '예술고등학교' : [('예술고등학교', '예고')],
           '중학교' : [('중학교', '중')],
           '고등학교' : [('고등학교', '고')],
           '초등학교' : [('초등학교', '초')],
           '여자대학교' : [('여자대학교', '여대')],
           '전문대학교' : [('전문대학교', '전문대')],
           '외국어대학교' : [('외국어대학교', '외대')],
           'university' : [('university', 'univ')],
           'kaist' : [('kaist', '카이스트'),('kaist','한국과학기술원')],
           '카이스트' : [('카이스트', '한국과학기술원')],
           }

    for key in dic:
        if key in name:
            for a, b in dic[key]:
                name_list.append(name.replace(a, b))

    return name_list


# MAKE_SAME_LIST
# delete unnecessary data
# make same_list
def MAKE_NAME_LIST(LIST, name_list):

    # consider as same in this list
    [name, name_other] = delete_unnecessary(LIST)

    if name:
        # 이름이 바뀌는 경우
        name_list = other_case(name, name_list)
        name_list.append(name)
    if name_other:
        # 이름이 바뀌는 경우
        name_list = other_case(name_other, name_list)
        name_list.append(name_other)

    return name_list

# data_processing
# find duplicate schools
def data_processing():

    # 같은 것 끼리 [id-id]로 저장되어 있다.
    Same_tuple_List = []

    # member_count가 0이라 지워지는 데이터
    Delete_list = []

    for idx, data in enumerate(SCHOOL_LIST):

        # 아무도 등록되어 있지 않은 학교는 삭제해도 된다.
        # meber_count = 0
        if int(data[9]) == 0:
            Delete_list.append(data[0])
            continue

        # 같은 이름이 저장 될 LIST
        name_list = []

        name_list = MAKE_NAME_LIST(data, name_list)

        for idx2, data_2 in enumerate(SCHOOL_LIST):

            if idx == idx2:
                continue

            name, name_other = delete_unnecessary(data_2)

            if name:
                if name in name_list:
                    Same_tuple_List.append([data[0], data_2[0]])
            if name_other:
                if name_other in name_list:
                    Same_tuple_List.append([data[0], data_2[0]])

    return Same_tuple_List, Delete_list

# 같은 id의 LIST를 만든다.
def Make_Same_List(done_list, same_list, data, S_DATA):
	Stack = []

	# Stack에다 제일 처음 값을 추가
	Stack.append(data)

	# Stack의 시작위치
	start = 0

	# Stack의 사이즈
	size = 1

	while start != size:
		for idx, data in enumerate(S_DATA):
			if data[0] == Stack[start] and data[1] not in Stack:
				Stack.append(data[1])
				size += 1

			if data[1] == Stack[start] and data[0] not in Stack:
				Stack.append(data[0])
				size += 1

		done_list.append(Stack[start])
		start += 1

	same_list.append(Stack)

	return done_list, same_list


# 값들을 연결한다.
def connect(Same_tuple_List, Delete_list):
    with open("학교데이터 삭제","w") as file:
        for data in Delete_list:
            for school in SCHOOL_LIST:
                if str(data) == str(school[0]):
                    for dt in school:
                        file.write("{0}\t".format(dt))
                    file.write("\n")
                    break

    with open("학교데이터 병합","w") as output:
        # 이미 한 번 체크한 데이터를 저장하는 LIST
        done_list = []
        # 같은 학교의 id가 저장되어 있는 LIST
        same_list = []

    	for idx, data in enumerate(Same_tuple_List):
    		if data[0] not in done_list:
    			done_list, same_list = Make_Same_List(done_list, same_list, data[0], Same_tuple_List)

    		if data[1] not in done_list:
    			done_list, same_list = Make_Same_List(done_list, same_list, data[1], Same_tuple_List)

        # 연결된 same_list를 출력
        for s_list in same_list:

            # 가장 큰 member_count
            max_count = -1

            # 그 가장 큰 member_count id
            connected_with = 0

            # 최대 member_count와 그 id를 찾는 과정
            for id in s_list:
                for idx, data in enumerate(SCHOOL_LIST):
                    if data[0] == id:
                        if max_count < int(data[9]):
                            max_count = int(data[9])
                            connected_with = id
                            break

    		# data를 출력한다.
            for id in s_list:
                for idx, data in enumerate(SCHOOL_LIST):
                    if data[0] == id:
                        data.append(connected_with)
                        for dt in data:
                            output.write("{0}\t".format(dt))
                        output.write("\n")
                        break



if __name__ == "__main__":

    # 학교 파일 이름
    FILE_NAME = "school20190425"

    # data_loading
    print("------------ loading data ---------------")
    data_loading(FILE_NAME)
    print("-----------------------------------------")
    # data_loading done

    Same_tuple_List, Delete_list = data_processing()

    print("processing done!")

    connect(Same_tuple_List, Delete_list)

    print("connecting done!")
