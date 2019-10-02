from sense_hat import SenseHat
sense = SenseHat()

green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

class scanner:
	def __init__(self):
		self.values = [0, 0, 0] #set default values to 0
		#Format: [Temperature, Humidity, Pressure]
		self.setBlackLight()
		self.update()

	def update(self):
		try:
			temp = sense.get_temperature_from_pressure()
		except:
			temp = -1
		try:
			humidity = round(sense.get_humidity(), 2) + 25.00
		except:
			humidity = -1
		
		try:
			pressure = round(sense.get_pressure(), 2)
		except:
			pressure = -1

		self.values = [temp, humidity, pressure]
	
	#check for joystick input. If yes, call for an update in the controller
	def checkJoyStick(self):
		events = sense.stick.get_events()
		for event in events:
			if event.action != "released":
				return True
		return False
	
	#setters for the lights
	#NB: It wouldn't work if I didn't have self included as an argument in the function!
	def setGreenLight(self):
		sense.clear(green)
	
	def setRedLight(self):
		sense.clear(red)
	
	def setYellowLight(self):
		sense.clear(yellow)
	
	def setBlackLight(self):
		sense.clear(black)
	
	def setWhiteLight(self):
		sense.clear(white)
	
	#getters for the individual values
	def getValues(self):
		return self.values
	
	def getTemp(self):
		return self.values[0]
	
	def getHumidity(self):
		return self.values[1]
	
	def getPressure(self):
		return self.values[2]
