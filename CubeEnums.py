class Color:
	WHITE = 0
	YELLOW = 1
	BLUE = 2
	GREEN = 3
	RED = 4
	ORANGE = 5

class Face:
	FRONT = 0
	BACK = 1
	UP = 2
	DOWN = 3
	RIGHT = 4
	LEFT = 5

	def opposite(face):
		if(face%2==0):
			return face+1
		else:
			return face-1