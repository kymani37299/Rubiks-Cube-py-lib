import CubeDrawer

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

class Side:

	'''
	:param color: Color enum , what color on that side
	'''
	def __init__(self,color):
		self.colors = [3*[color] for i in range(3)]

	'''
	Gets whole row

	:param row: Row number to get
	:rtype: array of 3 enum Color
	'''
	def get_row(self,row):
		data = []
		for i in range(3):
			data.append(self.colors[row][i])
		return data

	'''
	Sets whole row to data

	:param row: Row number to set
	:param data: array of 3 enum color
	'''
	def set_row(self,row,data):
		for i in range(3):
			self.colors[row][i] = data[i]

	'''
	Get whole column

	:param col: Column number to get
	:rtype: array of 3 enum Color
	'''
	def get_col(self,col):
		data = []
		for i in range(3):
			data.append(self.colors[i][col])
		return data


	'''
	Sets whole column to data

	:param col: Column number to set
	:param data: array of 3 enum color
	'''
	def set_col(self,col,data):
		for i in range(3):
			self.colors[i][col] = data[i]

	'''
	Rotate side
	:param clockwise: True for clockwise,False for counterclockwise
	'''
	def rotate(self,clockwise):
		edges = [(0,1),(1,2),(2,1),(1,0)]
		corners = [(0,0),(0,2),(2,2),(2,0)]

		if not clockwise:
			tmp = edges[0]
			edges[0] = edges[2]
			edges[2] = tmp
			tmp = corners[0]
			corners[0] = corners[2]
			corners[2] = tmp

		edge_tmp = self.colors[edges[3][0]][edges[3][1]]
		corner_tmp = self.colors[corners[3][0]][corners[3][1]]

		for i in range(4):
			tmp = self.colors[edges[i][0]][edges[i][1]]
			self.colors[edges[i][0]][edges[i][1]] = edge_tmp
			edge_tmp = tmp
			tmp = self.colors[corners[i][0]][corners[i][1]]
			self.colors[corners[i][0]][corners[i][1]] = corner_tmp
			corner_tmp = tmp


class Cube:

	def __init__(self):
		self.sides = {
			Face.FRONT: Side(Color.BLUE),
			Face.BACK: Side(Color.GREEN),
			Face.UP: Side(Color.YELLOW),
			Face.DOWN: Side(Color.WHITE),
			Face.RIGHT: Side(Color.RED),
			Face.LEFT: Side(Color.ORANGE)
		}
		self.history = []

	'''
	Performs one move
	List of possible moves: (x y z F B R L U D M S E f r b r l u d) 
	(works with F B R L U D for now (with 2 and '))
	and all these with '(ex. R') and 2(ex. R2)
	
	:param move: string with length of 2 that represents a move
	'''
	def perform_move(self,move):
		get_function = lambda side,row,col: side.get_row(row) if row != -1 else side.get_col(col)
		set_function = lambda side,row,col,data: side.set_row(row,data) if row != -1 else side.set_col(col,data)
		double_move = False
		clockwise = True

		if(move[0]=='R'):
			faces = [Face.FRONT,Face.UP,Face.BACK,Face.DOWN]
			main_face = Face.RIGHT
			row = [-1]*4
			col = [2]*4
			col[2] = 0
		elif(move[0]=='L'):
			faces = [Face.FRONT,Face.DOWN,Face.BACK,Face.UP]
			main_face = Face.LEFT
			row = [-1]*4
			col = [0]*4
			col[2] = 2
		elif(move[0]=="U"):
			faces = [Face.FRONT,Face.LEFT,Face.BACK,Face.RIGHT]
			main_face = Face.UP
			row = [0]*4
			col = [-1]*4
		elif(move[0]=="D"):
			faces = [Face.FRONT,Face.RIGHT,Face.BACK,Face.LEFT]
			main_face = Face.DOWN
			row = [2]*4
			col = [-1]*4
		elif(move[0]=="F"):
			faces = [Face.UP,Face.RIGHT,Face.DOWN,Face.LEFT]
			main_face = Face.FRONT
			row = [2,-1,0,-1]
			col = [-1,0,-1,2]
		elif(move[0]=="B"):
			faces = [Face.UP,Face.LEFT,Face.DOWN,Face.RIGHT]
			main_face = Face.BACK
			row = [0,-1,2,-1]
			col = [-1,0,-1,2]
		elif(move[0]=="M"):
			faces = [Face.UP,Face.FRONT,Face.DOWN,Face.BACK]
			row = [-1]*4
			col = [1]*4
			main_face = None
		else:
			print("ERROR INVALID MOVE {}".format(move))
			return

		if(len(move)>1):
			if(move[1]=="'"):
				tmp = faces[0]
				faces[0] = faces[2]
				faces[2] = tmp
				tmp = row[0]
				row[0] = row[2]
				row[2] = tmp
				tmp = col[0]
				col[0] = col[2]
				col[2] = tmp
				clockwise = False
			elif(move[1]=="2"):
				double_move = True

		while True:
			if main_face:
				self.sides[main_face].rotate(clockwise)
			tmp = get_function(self.sides[faces[3]],row[3],col[3])
			for i in range(4):
				tmp2 = get_function(self.sides[faces[i]],row[i],col[i])
				set_function(self.sides[faces[i]],row[i],col[i],tmp)
				tmp = tmp2

			if not double_move:
				break
			double_move = False

		self.history.append(move[0:min(2,len(move))])


	def perform_alg(self,alg):
		moves = alg.split(" ")
		for move in moves:
			move = move.strip()
			self.perform_move(move)

	def undo(self):
		if(len(self.history)>0):
			last_move = self.history[-1]
			self.history = self.history[:-1]
			if(len(last_move)>1 and last_move[1]=="'"):
				last_move = last_move[0]
			else:
				last_move += "'"
			self.perform_move(last_move)
			self.history = self.history[:-1]

	def show(self):
		CubeDrawer.show(self,str(" ".join(map(str, self.history))))

if __name__ == "__main__":
	cube = Cube()
	cube.show()