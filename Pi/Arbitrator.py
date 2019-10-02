import json

class arbitrator:
	@staticmethod
	def evaluate_data(data):
		j = json.loads(data)
		arr = [0, 0, 0]
		arr[0] = j['temp:']
		arr[1] = j['humidity:']
		arr[2] = j['airPressure:']
		
		#no sound
		min_values = [20, 30, 1000]
		max_values = [22.5, 50, 1030]

		booleans = [True, True, True]
		if (arr[0] < min_values[0] or arr[0] > max_values[0]):
			booleans[0] = False
		if (arr[1] < min_values[1] or arr[1] > max_values[1]):
			booleans[1] = False
		if (arr[2] < min_values[2] or arr[2] > max_values[2]):
			booleans[2] = False

		return booleans

	@staticmethod
	def choose_action(arr):
		booleans = arbitrator.evaluate_data(arr)
		False_count = 0
		for i in range(3):
                        if booleans[i] == False:
                                False_count += 1

		#if 0 values are false, there will be green lights.
		#if 1 value is false, there will be yellow lights. (?)
		#if more than one value is false, there will be red lights.
		#This can be implemented differently, if needed. This Arbitrator class is only a prototype.
		if False_count == 0:
			return "good"
		else:
			return "bad"
