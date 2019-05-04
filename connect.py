# -*- coding:utf-8 -*-

COMPANY_FILE_NAME = "company20190417"
CORRECT_DATA_FILE_NAME = "correct_data_backup"

COMPANY_DATA = []
CORRECT_DATA = []

output = open("CONNECT_COMAPNY_OUTPUT","w")


if __name__ == "__main__":
	with open(COMPANY_FILE_NAME,"r") as file:
		COMPANY_DATA = file.read().splitlines()

	with open(CORRECT_DATA_FILE_NAME,"r") as file:
		CORRECT_DATA = file.read().splitlines()

	for idx, data in enumerate(COMPANY_DATA):
		COMPANY_DATA[idx] = data.split("\t")

	for idx, data in enumerate(CORRECT_DATA):
		CORRECT_DATA[idx] = data.split("\t")

	done_list = []
	same_list = []

	for idx, data in enumerate(CORRECT_DATA):
		Stack = []

		if data[0] not in done_list:
			Stack.append(data[0])
			start = 0
			size = 1
			while start != size:
				for idx, data in enumerate(CORRECT_DATA):
					if data[0] == Stack[start] and data[1] not in Stack:
						Stack.append(data[1])
						size += 1

					if data[1] == Stack[start] and data[0] not in Stack:
						Stack.append(data[0])
						size += 1
				done_list.append(Stack[start])
				start += 1

			same_list.append(Stack)

		Stack = []

		if data[1] not in done_list:
			Stack.append(data[1])
			start = 0
			size = 1
			while start != size:
				for idx, data in enumerate(CORRECT_DATA):
					if data[0] == Stack[start] and data[1] not in Stack:
						Stack.append(data[1])
						size += 1

					if data[1] == Stack[start] and data[0] not in Stack:
						Stack.append(data[0])
						size += 1
				done_list.append(Stack[start])
				start += 1

			same_list.append(Stack)


	for s_list in same_list:
		max_weight = 0
		connected_with = 0

		for id in s_list:
			for idx, data in enumerate(COMPANY_DATA):
				if data[0] == id:
					if max_weight < int(data[11]):
						max_weight = int(data[11])
						connected_with = id
					break

		for id in s_list:
			for idx, data in enumerate(COMPANY_DATA):
				if data[0] == id:
					data[12] = connected_with
					for dt in data:
						output.write("{0}\t".format(dt))
					output.write("\n")
					break
	output.close()
