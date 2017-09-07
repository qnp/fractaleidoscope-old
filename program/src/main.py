# Juste un petit programme pour essayer:
# changer les effets avec la touche c
# quitter avec q

import cv2
import sys
import numpy as np
import math

VP_WIDTH = 1280
VP_HEIGHT = 800
SCREEN_W = 998
N_DELAY = 10 #DELAY OU PAS?  10
chan = 3
grande = np.empty([VP_HEIGHT,VP_WIDTH,chan],dtype=np.uint8)
bigBuff = np.empty([N_DELAY,VP_HEIGHT,VP_WIDTH,chan],dtype=np.uint8)
quarter = np.empty([VP_HEIGHT/2,VP_WIDTH/2,chan])

#VP_WIDTH = 1920
#VP_HEIGHT = 1080

if VP_WIDTH%2:
	raise ValueError('VP_WIDTH must be dividable by 2')
	if VP_HEIGHT%2:
		raise ValueError('VP_HEIGHT must be dividable by 2')

#renvoie le nom de la fenetre
def getNameWindow(ind):
	return 'capture, effet = '+str(ind)

#miroir droite gauche qui ecrase la moitie de l image
def mirrorlrHalf():
	global im,grande,VP_WIDTH,VP_HEIGHT
	height, width, chan = im.shape
	im[0:height,width/2:width,0:chan] = np.fliplr(im[0:height,0:width/2,0:chan])
	grande[VP_HEIGHT/2-height/2:VP_HEIGHT/2+height/2,VP_WIDTH/2-width/2:VP_WIDTH/2+width/2,0:chan]=im #/255

#miroir droite gauche haut bas qui ecrase la moitie de l image
def mirrorlrudHalf():
	global im,grande,VP_WIDTH,VP_HEIGHT
	height, width, chan = im.shape
	im[0:height/2,width/2:width,0:chan] = np.fliplr(im[0:height/2,0:width/2,0:chan])
	im[height/2:height,0:width,0:chan] = np.flipud(im[0:height/2,0:width,0:chan])
	grande[VP_HEIGHT/2-height/2:VP_HEIGHT/2+height/2,VP_WIDTH/2-width/2:VP_WIDTH/2+width/2,0:chan]=im #/255
	#im[height/2:height,0:width,0:chan]= im[0:height/2,0:width,0:chan];

#miroir droite gauche qui garde tout
def mirrorlr():
	global im,grande,VP_WIDTH,VP_HEIGHT
	height, width, chan = im.shape
	temp = np.fliplr(im[0:height,0:width/2,0:chan])
	im[0:height,0:width/2,0:chan] = np.fliplr(im[0:height,width/2:width,0:chan])
	im[0:height,width/2:width,0:chan] = temp
	grande[VP_HEIGHT/2-height/2:VP_HEIGHT/2+height/2,VP_WIDTH/2-width/2:VP_WIDTH/2+width/2,0:chan]=im #/255

#duplicate 4 times the cam image + mirror them
def dupliquad():
	global im,grande,quarter,VP_WIDTH,VP_HEIGHT
	height, width, chan = im.shape
	im=im #/255
	#grande = np.empty([VP_HEIGHT,VP_WIDTH,chan])
	#quarter = np.empty([VP_HEIGHT/2,VP_WIDTH/2,chan])
	#print(quarter.shape)
	#print(im[height/2-VP_HEIGHT/4:height/2+VP_HEIGHT/4,width/2-VP_WIDTH/4:width/2+VP_WIDTH/4,0:chan].shape)
	#print(quarter[VP_HEIGHT/2-height:VP_HEIGHT/2,VP_WIDTH/2-width:VP_WIDTH/2,0:chan].shape)
	if VP_HEIGHT<=2*height and VP_WIDTH<=2*width:
		quarter = im[height/2-VP_HEIGHT/4:height/2+VP_HEIGHT/4,width/2-VP_WIDTH/4:width/2+VP_WIDTH/4,0:chan]
		if VP_HEIGHT>2*height and VP_WIDTH>2*width:
			quarter[VP_HEIGHT/2-height:VP_HEIGHT/2,VP_WIDTH/2-width:VP_WIDTH/2,0:chan] = im
	grande[0:VP_HEIGHT/2,0:VP_WIDTH/2,0:chan] = quarter; #N-O
	grande[0:VP_HEIGHT/2,VP_WIDTH/2:VP_WIDTH,0:chan] = np.fliplr(quarter); #N-E
	grande[VP_HEIGHT/2:VP_HEIGHT,VP_WIDTH/2:VP_WIDTH,0:chan] = np.flipud(np.fliplr(quarter)); #S-E
	grande[VP_HEIGHT/2:VP_HEIGHT,0:VP_WIDTH/2,0:chan] = np.flipud(quarter); #S-O
	#grande[height:2*height,0:width,0:chan] = im;
	#grande[height:2*height,width:2*width,0:chan] = im;
	#return grande

def adjustScreen():
	global grande
	grande[0:VP_HEIGHT,0:(VP_WIDTH-SCREEN_W)/2] = 0
	grande[0:VP_HEIGHT,(VP_WIDTH+SCREEN_W)/2:VP_WIDTH] = 0
	
def preventTooMuchLumin():
	global grande
	maxLum = VP_HEIGHT*VP_WIDTH*chan*255
	limitLum = 0.3*maxLum
	lumin = np.sum(grande)
	if lumin > limitLum:
		#print("yo")
		#grande[:,:,0:3] *= 0.7
		grande[:,:,0] = cv2.equalizeHist(grande[:,:,0])
		grande[:,:,1] = cv2.equalizeHist(grande[:,:,1])
		grande[:,:,2] = cv2.equalizeHist(grande[:,:,2])
		#grande[:,:,0:3] *= 0.7
		#for i in range(0, VP_HEIGHT):
		#	for j in range(0, VP_WIDTH):
		#		grande[i,j,0:3]/=10
				#if grande[i][j][0]<=limitLum and grande[i][j][1]<=limitLum and grande[i][j][2]<=limitLum:
			    #		grande[i][j][0:3] = 0

def adjustLumin():
	global grande
	grande[:,:,0] = cv2.equalizeHist(grande[:,:,0])
	grande[:,:,1] = cv2.equalizeHist(grande[:,:,1])
	grande[:,:,2] = cv2.equalizeHist(grande[:,:,2])
	#grande[:,:,1] = 0
	#grande[:,:,2] = 0
	ret,grande = cv2.threshold(grande,50,255,cv2.THRESH_TOZERO)

countNoLarsen = 0
def preventNoLarsen():
	global grande,countNoLarsen
	lumin = np.sum(grande)
	limMin = 20000000
	nCounts = 300
	if lumin < limMin:
		countNoLarsen+=1
		if countNoLarsen >= nCounts:
 			grande[:,:,:] = 80
			if countNoLarsen >= nCounts+N_DELAY:
				countNoLarsen = 0


#applique un effet miroir selon l'indice et redimmensionne.
def fractalize(ind):
	if ind==0:
		pass
	elif ind==1:
		mirrorlrHalf()
	elif ind==2:
		mirrorlr()
	elif ind==3:
		mirrorlrudHalf()
	elif ind==4:
		dupliquad()
	#m= cv2.bitwise_and(im,mask)
	#return im;

#settings de la camera:
video_capture = cv2.VideoCapture(0)
#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT,960)

junk, im = video_capture.read()
print(im.shape)
#print(type(im[0][0][0]))
#print(type(grande[0][0][0]))

#settings du mask: (pour essayer d'occulter avec un triangle => pas concluant)
#mask =cv2.imread("mask.png");
#mask=cv2.resize(mask,(width,height) );

#setting de la fonction miroir:
indMir=4
maxInd=5

#boucl#e
modFrames=1
idFrame=0
idBuff=0
canDisplay=False
while True:
	idFrame+=1
	if idFrame%modFrames==0:
		ret, im = video_capture.read()
		fractalize(indMir)
		cv2.namedWindow(getNameWindow(indMir), cv2.WND_PROP_FULLSCREEN)
		cv2.setWindowProperty(getNameWindow(indMir), cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
		#if indMir == 4:
		adjustLumin() #ADJUST OU PAS ou autre fonction
		adjustScreen()
		#preventTooMuchLumin()
		preventNoLarsen()
		bigBuff[idBuff,:,:,:]=grande[:,:,:]
		idBuff+=1
		if idBuff==N_DELAY:
			idBuff=0
			canDisplay=True
		if canDisplay:
			cv2.imshow(getNameWindow(indMir),bigBuff[idBuff,0:800,0:1280,0:3])
		#cv2.imshow(getNameWindow(indMir),grande[0:800,0:1280,0:3])
		#else:
		#im = cv2.resize(im,(1280,800))
		#cv2.imshow(getNameWindow(indMir),im)
		key = (cv2.waitKey(1)&255)
		if key:
			#if key == ord('c'):
			#	cv2.destroyWindow( getNameWindow(indMir))
			#	indMir= (indMir + 1)%maxInd
			if key == ord('q'):
				break
