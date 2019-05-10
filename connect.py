# -*- coding:utf-8 -*-
'''
	same_data 에 있는 데이터들을 연결시킨다.
'''

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

# same_data의 리스트를 연결한다.
def Connect_data(COMPANY_DATA):

	SAME_DATA = []

	with open("same_data","r") as file:
		SAME_DATA = file.read().splitlines()

	for idx, data in enumerate(SAME_DATA):
		SAME_DATA[idx] = data.split("\t")

	# 이미 한 번 체크한 데이터를 저장하는 LIST
	done_list = []

	# 같은 기업의 id가 저장되어 있는 LIST
	same_list = []

	for idx, data in enumerate(SAME_DATA):
		if data[0] not in done_list:
			done_list, same_list = Make_Same_List(done_list, same_list, data[0], SAME_DATA)

		if data[1] not in done_list:
			done_list, same_list = Make_Same_List(done_list, same_list, data[1], SAME_DATA)

	# clear FILE
	with open("자동처리","w") as file:
		pass

	with open("수동처리","w") as file:
		pass

	# 연결된 same_list를 출력
	for s_list in same_list:

		# 가장 큰 weight
		max_weight = 0

		# 두 번째로 큰 weigth
		second_max_weight = 0

		# 그 가장 큰 weight의 id
		connected_with = 0

		# 최대 Weight과 그 id를 찾는 과정
		for id in s_list:
			for idx, data in enumerate(COMPANY_DATA):
				if data[0] == id:
					if max_weight < int(data[11]):

						# 두 번째로 큰 것에 현재 max weight을 준다.
						second_max_weight = max_weight

						max_weight = int(data[11])
						connected_with = id

					elif int(data[11]) <= max_weight and int(data[11]) >= second_max_weight:
						second_max_weight = int(data[11])

					break

		# data를 출력한다.
		# 지워야 될 것이 가중치 4 이상이라면 수동처리
		if second_max_weight >= 4:
			with open("수동처리","a") as output:
				for id in s_list:
					for idx, data in enumerate(COMPANY_DATA):
						if data[0] == id:
							data[12] = connected_with
							for iter in range(len(COMPANY_DATA[idx])-1):
								output.write("{0}\t".format(COMPANY_DATA[idx][iter]))
							output.write("\n")
							break
		# 아닌경우 자동처리
		else:
			with open("자동처리","a") as output:
				for id in s_list:
					for idx, data in enumerate(COMPANY_DATA):
						if data[0] == id:
							data[12] = connected_with
							for iter in range(len(COMPANY_DATA[idx])-1):
								output.write("{0}\t".format(COMPANY_DATA[idx][iter]))
							output.write("\n")
							break
