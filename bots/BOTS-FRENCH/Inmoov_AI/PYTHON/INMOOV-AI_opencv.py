# -*- coding: utf-8 -*- 

from decimal import Decimal
global FaceDetectedCounter
FaceDetectedCounter=0
global FaceDetected 
FaceDetected=1
global startTimerFunction
global posxSquare 
global posySquare 
global WidthSquare 
WidthSquare=Decimal(0)
global FaceHadMoved
FaceHadMoved=0
posxSquare=Decimal(0)
posySquare=Decimal(0)
python.subscribe(opencv.getName(),"publishOpenCVData")


NoFaceDetectedTimer = Runtime.start("NoFaceDetectedTimer","Clock")
NoFaceDetectedTimer.setInterval(20000)

def onOpenCVData(data):
#This is opencv functions that do jobs

	global posxSquare
	global posySquare
	global openCvModule
	global WidthSquare
	global FaceHadMoved
	global FaceDetectedCounter
# openCvModule=="photo" : just detect one face
	if openCvModule=="photo":

		
		
		if data.getBoundingBoxArray() != None:
			if not data.getBoundingBoxArray():
				FaceDetectedCounter=0
			else:
				FaceDetectedCounter+=1
				if FaceDetectedCounter>50 and FaceDetected==0:
					NoFaceDetectedTimer.stopClock()
					FaceDetected=1
					chatBot.getResponse("SYSTEM FACEDETECTED")

# openCvModule=="123" : just detect if detected face is mooving in the space. 1.2.3 soleil :)
	if openCvModule=="123":
		#Tweak speed movement of the head
		openCvModulesensibilityLeftRightMin=0.05
		openCvModulesensibilityLeftRightMax=0.2
		openCvModulesensibilityFrontBackMin=0.01
		openCvModulesensibilityFrontBackMax=0.1
		#if something is detected
		if data.getBoundingBoxArray() != None:
			if data.getBoundingBoxArray():
				#get the first face detected
				rect = data.getBoundingBoxArray().get(0)
				MoveLeftRight=abs(posxSquare-Decimal(rect.x))
				#just to tune the demo detect if it's a left or right move
				MoveTopBottom=abs(posySquare-Decimal(rect.y))
				MoveFrontBack=abs(WidthSquare-Decimal(rect.width))
				#We wait to be sure it is not artefact
				FaceDetectedCounter+=1
								
				if FaceDetectedCounter>10:
					#ok we detect i the face move left/right/front/back
					if posxSquare != 0 and Decimal(rect.x) != 0 and Decimal(rect.y) != 0 and Decimal(rect.width) != 0 and MoveFrontBack < openCvModulesensibilityFrontBackMax and MoveTopBottom < openCvModulesensibilityLeftRightMax and MoveLeftRight < openCvModulesensibilityLeftRightMax and posySquare != 0 and MoveLeftRight !=0 and MoveTopBottom !=0:
						print MoveFrontBack
						#left/right move
						#tune demo 
						MoveX=0
						MoveY=0
						MoveZ=0
						if ((MoveLeftRight >= openCvModulesensibilityLeftRightMin ) or (MoveTopBottom >= openCvModulesensibilityLeftRightMin ) or (MoveFrontBack>=openCvModulesensibilityFrontBackMin )):
							
							if MoveLeftRight >= openCvModulesensibilityLeftRightMin:
									
								if posxSquare-Decimal(rect.x)>0:
									MoveX="Left"
								else:
									MoveX="Right"
									
							if MoveTopBottom >= openCvModulesensibilityLeftRightMin:
									
								if posySquare-Decimal(rect.y)>0:
									MoveY="Top"
								else:
									MoveY="Bottom"
									
							if MoveFrontBack>=openCvModulesensibilityFrontBackMin:
									
								if WidthSquare-Decimal(rect.width) >0:
									MoveZ="Front"
								else:
									MoveZ="Back"
									
							print "MOVE DETECTED :",MoveLeftRight,MoveTopBottom,MoveFrontBack,MoveX,MoveY,MoveZ
							talk("Tu as bougé!")
							FaceDetectedCounter=0
																						# Store the information in rect
					else:
						FaceDetectedCounter=0
					posxSquare = Decimal(rect.x)                                        # Get the x position of the corner
					posySquare = Decimal(rect.y)                                       # Get the y position of the corner
					WidthSquare = Decimal(rect.width)                                    # Get the width
					h = rect.height
					
					
			else:
				FaceDetectedCounter=0
				
		
		
	

StopListenTimer.addListener("pulse", python.name, "StopListenTimerFunc")
# start the clock
StopListenTimer.startClock()
				
				
				
			
	
		
def NoFaceDetectedTimerFunction(timedata):
	global startTimerFunction
	startTimerFunction+=1
	if startTimerFunction==2:
		FaceDetected=1
		chatBot.getResponse("SYSTEM FACENOTDETECTED")
		
		
				
NoFaceDetectedTimer.addListener("pulse", python.name, "NoFaceDetectedTimerFunction")
# start the clock

def trackHumans():
	#i01.headTracking.findFace()
	#i01.opencv.SetDisplayFilter
	i01.headTracking.faceDetect()
	i01.eyesTracking.faceDetect()
	print "test"

def TakePhoto(messagePhoto):
	i01.startEyesTracking(leftPort,22,24)
	i01.eyesTracking.faceDetect()	
	talkBlocking(messagePhoto)
	global openCvModule
	openCvModule = "photo"
	global FaceDetected
	global FaceDetectedCounter
	global startTimerFunction
	FaceDetectedCounter=0
	FaceDetected=0
	Light(0,0,0)
	startTimerFunction=0
	NoFaceDetectedTimer.startClock()


def PhotoProcess(messagePhoto):
	global FaceDetected
	Light(1,1,1)
	FaceDetectedCounter=0
	FaceDetected=1
	NoFaceDetectedTimer.stopClock()
	NeoPixelF(3)
	talkBlocking(messagePhoto)
	Light(1,1,1)
	talkBlocking("chi i i i i i i i i ize")
	sleep(0.5)
	Light(0,0,0)
	sleep(0.1)
	Light(1,1,1)
	sleep(0.1)
	Light(0,0,0)
	sleep(0.1)
	Light(1,1,1)
	sleep(0.1)
	i01.stopTracking()
	opencv.removeFilters()
	opencv.stopCapture()
	sleep(1)
	opencv.setInputSource("camera")
	opencv.setCameraIndex(0)
	opencv.capture()
	sleep(0.5)
	Light(0,0,0)
	photoFileName = opencv.recordSingleFrame()
	#print "name file is" , os.getcwd()+'\\'+str(photoFileName)
	Light(1,1,1)
	NeoPixelF(1)
	DisplayPic(os.getcwd()+'\\'+str(photoFileName))
	opencv.removeFilters()
	opencv.stopCapture()
	#i01.startEyesTracking(leftPort,22,24)
	#i01.startHeadTracking(leftPort)
	
if DEBUG==1:
	openCvModule="123"
	i01.opencv.setCameraIndex(0)
	i01.opencv.removeFilters()
	i01.opencv.addFilter("PyramidDown")
	i01.opencv.addFilter("Gray")
	i01.opencv.addFilter("FaceDetect")
	i01.opencv.setDisplayFilter("FaceDetect")
	i01.opencv.capture()
	