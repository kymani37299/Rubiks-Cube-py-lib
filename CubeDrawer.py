import numpy as np
import matplotlib.pyplot as plt
import cv2
from CubeEnums import *

# Size of one side of rubiks cube 
SIDE_SIZE = 200
STICKER_SIZE = int(SIDE_SIZE/3)
IMG_SIZE = (SIDE_SIZE*3+2,SIDE_SIZE*4+2)

COLOR_MAP_BGR = {
	Color.WHITE: (1,1,1),
	Color.YELLOW: (0,1,1),
	Color.BLUE:  (1,0,0),
	Color.GREEN: (0,1,0),
	Color.RED: (0,0,1),
	Color.ORANGE: (0,0.64,1)
}

COLOR_MAP_RGB = {
	Color.WHITE: (1,1,1),
	Color.YELLOW: (1,1,0),
	Color.BLUE:  (0,0,1),
	Color.GREEN: (0,1,0),
	Color.RED: (1,0,0),
	Color.ORANGE: (1,0.64,0)
}

'''
Draws a cube on screen

:param cube: Instance of Cube class
'''
def show(cube,interactive=False):
	global COLOR_MAP
	if(interactive):
		COLOR_MAP = COLOR_MAP_BGR
		_run_cv2(cube)
	else:
		COLOR_MAP = COLOR_MAP_RGB
		_run_pyplot(cube)
	
	

def _update_image(cube):
	image = np.ones((IMG_SIZE[0],IMG_SIZE[1],3))*(0.5,0.5,0.5)
	faces = [Face.FRONT,Face.BACK,Face.UP,Face.DOWN,Face.RIGHT,Face.LEFT]
	for face in faces:
		_color_face(image,face,cube.sides[face])
	return image


def _run_cv2(cube):
	key = 0
	while _controls(key,cube):
		image = _update_image(cube)
		screen = cv2.imshow("Rubik's cube",image)
		key = cv2.waitKey(25) & 0xFF

# TODO: Draw move history on top of the image
def _run_pyplot(cube):
	image = np.array(_update_image(cube))
	fig = plt.imshow(image)

	# Turn off axis
	plt.axis('off')
	fig.axes.get_xaxis().set_visible(False)
	fig.axes.get_yaxis().set_visible(False)

	plt.show()

		
		

def _controls(key,cube):
	if(key == ord('q') or key == ord('Q')):
		cv2.destroyAllWindows()
		return False
	elif(key == ord('0')):
		cube.undo()
	elif(key == ord('r')):
		cube.perform_move("R")
	elif(key== ord('R')):
		cube.perform_move("R'")
	elif(key == ord('l')):
		cube.perform_move("L")
	elif(key== ord('L')):
		cube.perform_move("L'")
	elif(key == ord('f')):
		cube.perform_move("F")
	elif(key== ord('F')):
		cube.perform_move("F'")
	elif(key == ord('b')):
		cube.perform_move("B")
	elif(key== ord('B')):
		cube.perform_move("B'")
	elif(key == ord('u')):
		cube.perform_move("U")
	elif(key== ord('U')):
		cube.perform_move("U'")
	elif(key == ord('d')):
		cube.perform_move("D")
	elif(key== ord('D')):
		cube.perform_move("D'")
	elif(key == ord('m')):
		cube.perform_move("M")
	elif(key== ord('M')):
		cube.perform_move("M'")
	return True

'''
Colors face with colors data

:param image: np array of RGB image
:param face: face to color
:param side: instance of Side
'''
def _color_face(image,face,side):
	for i in range(3):
		for j in range(3):
			_color_sticker(image,face,(i,j),side.colors[i][j])


'''
Colors sticker on given face and position

:param image: np array of RGB image
:param face: face where sticker is located (enum Face)
:param position: position where sticker is located on face given as a (x,y) tuple (from (0,0) to (2,2))
:param color: color of sticker (enum Color)
'''
def _color_sticker(image,face,position,color):

	# Face to pos
	if(face == Face.UP):
		face_x = 0
		face_y = SIDE_SIZE
	elif(face == Face.DOWN):
		face_x = SIDE_SIZE*2
		face_y = SIDE_SIZE
	else:
		face_x = SIDE_SIZE
		if(face == Face.LEFT):
			face_y = 0
		elif(face == Face.FRONT):
			face_y = SIDE_SIZE
		elif(face == Face.RIGHT):
			face_y = SIDE_SIZE*2
		else:
			face_y = SIDE_SIZE*3

	# Sticker to pos
	sticker_x = STICKER_SIZE*position[0]
	sticker_y = STICKER_SIZE*position[1]

	paint_x = face_x + sticker_x
	paint_y = face_y + sticker_y

	for i in range(STICKER_SIZE):
		for j in range(STICKER_SIZE):
			if(i==0 or i==STICKER_SIZE-1 or j==0 or j==STICKER_SIZE-1):
				image[paint_x+i+1][paint_y+j+1] = (0,0,0)
			else:
				image[paint_x+i+1][paint_y+j+1] = COLOR_MAP[color]


				
if __name__ == "__main__":
	cube = Cube()
	cube.perform_alg("F R U R' U' F'")
	cube.show()