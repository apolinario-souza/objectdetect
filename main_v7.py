import cv2
import numpy as np
from mylibraryopencv import findColor, getContours, drawOnCanvas, stackImages, empty

frameWidth = 640
frameHeight = 480

width_cm = 10 #value actual in cm

myColorValues = [[0,0,255]] #Red color

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)


mx = [0]
my = [0]

#click event function
def click_event(event, x, y, flags, param):
    
    if event == cv2.EVENT_LBUTTONDOWN:   
    
        mx.append(x)
        my.append(y)
    

 
 
myPoints =  [] 
font = cv2.FONT_HERSHEY_PLAIN


#Get object

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max","TrackBars",19,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",110,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",240,255,empty)
cv2.createTrackbar("Val Min","TrackBars",153,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)
 
while True:
    _,img = cap.read()
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    
    #myColors = [h_min, h_max, s_min, s_max, v_min, v_max]
    
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)

    cv2.putText(img,'Original',(int(frameWidth/2)+20,int(frameHeight/2)), font, 1,(0,255,255),2,cv2.LINE_AA)

    cv2.putText(imgHSV,'HSV',(int(frameWidth/2)+20,int(frameHeight/2)), font, 1,(0,255,255),2,cv2.LINE_AA)

    cv2.putText(mask,'Mask',(int(frameWidth/2)+20,int(frameHeight/2)), font, 1,(0,255,255),2,cv2.LINE_AA)

    cv2.putText(imgResult,'Result',(int(frameWidth/2)+20,int(frameHeight/2)), font, 1,(0,255,255),2,cv2.LINE_AA)
 
    imgStack = stackImages(0.6,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("Stacked Images", imgStack)
    

    key = cv2.waitKey(1)
    if key == 27:
        break

#cap.release()
cv2.destroyAllWindows()


myColors = [[h_min, h_max, s_min, s_max, v_min, v_max]]




#get actual distance 

while True:
    _,position = cap.read()


    actualx_stop = int(frameWidth/6)

    cv2.putText(position,'0 cm',(int(frameWidth/6)-50,200), font, 1,(0,0,255),2,cv2.LINE_AA) #Start text


    cv2.line(position,(int(frameWidth/6),0),(int(frameWidth/6),frameHeight),(0,0,255),3) #Start line
	



    if len (mx) > 1:        
        actualx_stop = mx[len (mx)-1]


    cv2.putText(position,'10 cm',(actualx_stop-55,200), font, 1,(0,0,255),2,cv2.LINE_AA) #Stop text

    cv2.line(position,(actualx_stop,0),(actualx_stop,frameHeight),(0,0,255),3) #Stop line

    cv2.putText(position,'ESC to confirm!',(int(frameWidth/2),int(frameHeight/8)), font, 1,(0,255,255),2,cv2.LINE_AA) #Stop text   
        
    cv2.imshow("Actual width", position)   
       
    #Get click
    cv2.setMouseCallback("Actual width", click_event)  
           
            
    
    key = cv2.waitKey(1)
    
    if key == 27:
        break

cv2.destroyAllWindows()


#star experiment
totalPoints_x = []
totalPoints_y = []
while True:
    success, img = cap.read()

    cv2.putText(img,'Target!',(int(frameWidth/2)+20,int(frameHeight/2)), font, 1,(0,255,255),2,cv2.LINE_AA) #S
        
    cv2.circle(img,(int(frameWidth/2),int(frameHeight/2)), 2, (0,0,255), cv2.FILLED) #target

    newPoints = findColor(img, myColors,myColorValues)
    

    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
            totalPoints_x.append(newP[0])
            totalPoints_y.append(newP[1])    

    cv2.imshow("Result", img)
      
    key = cv2.waitKey(1)
    
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()



#make process data

goalx = int (frameWidth/2)
goaly = int (frameHeight/2)


factor = width_cm/abs(actualx_stop - int(frameWidth/6))
errors_x = []
for error in totalPoints_x:
	errors_x.append(abs(error-goalx)*factor)

errors_y = []
for error in totalPoints_y:
	errors_y.append(abs(error-goaly)*factor)
	

print(errors_x)
