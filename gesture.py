import cv2
import numpy as np 
import math
import pyautogui as p
import time as t


#Read Camera
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

thresh = 0

def mythresh(val):
    global thresh
    thresh = val

#window name
cv2.namedWindow("Color Adjustments",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Color Adjustments", (300, 300)) 
cv2.createTrackbar("Thresh", "Color Adjustments", 0, 255, mythresh)

#COlor Detection Track

hueLow = 10
hueHigh = 179
huelowtwo = 10
huehightwo = 179
satLow = 10
satHigh = 255
valLow = 10
valHigh = 255

def myhuelow(val):
    global hueLow
    hueLow = val

def myhuehigh(val):
    global hueHigh
    hueHigh = val
def mysathigh(val):
    global satHigh
    satHigh = val

def myvallow(val):
    global valLow
    valLow = val

def myvalhigh(val):
    global valHigh
    valHigh = val

cv2.namedWindow("Color Adjustments")
cv2.createTrackbar("hueLow","Color Adjustments",10,179,myhuelow)
cv2.createTrackbar("hueHigh","Color Adjustments",10,179,myhuehigh)
cv2.createTrackbar("hueLowTwo","Color Adjustments",10,179,myhuelowtwo)
cv2.createTrackbar("hueHighTwo","Color Adjustments",10,179,myhuehightwo)
cv2.createTrackbar("satLow","Color Adjustments",10,255,mysatlow)
cv2.createTrackbar("satHigh","Color Adjustments",250,255,mysathigh)
cv2.createTrackbar("valLow","Color Adjustments",10,255,myvallow)
cv2.createTrackbar("valHigh","Color Adjustments",250,255,myvalhigh)


while True:
    _,frame = cap.read()
    frame = cv2.flip(frame,2)
    frame = cv2.resize(frame,(600,500))

    #step -1
    # Get hand data from the rectangle sub window
    cv2.rectangle(frame, (0,1), (300,500), (255, 0, 0), 0)
    crop_image = frame[1:500, 0:300]
    
    #Step -2
    hsv = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
    #detecting hand
    lowerbound = np.array([hueLow,satLow,valLow])
    upperbound = np.array([hueHigh,satHigh,valHigh])
    lowerboundtwo = np.array([huelowtwo,satLow,valLow])
    upperboundtwo = np.array([huehightwo,satHigh,valHigh])
    
    #Step - 4
    #Creating Mask
    mask = cv2.inRange(hsv, lowerbound, upperbound)
    mysecondmask = cv2.inRange(hsv,lowerboundtwo,upperboundtwo)
    #filter mask with image
    mynewmask = mask | mysecondmask
    filtr = cv2.bitwise_and(hsv,hsv,mask=mynewmask)
    
    #Step - 5
    mask1  = cv2.bitwise_not(mask)
    m_g = cv2.getTrackbarPos("Thresh", "Color Adjustments") #getting track bar value
    ret,thresh = cv2.threshold(mask1,m_g,255,cv2.THRESH_BINARY)
    dilata = cv2.dilate(thresh,(3,3),iterations = 6)
    
    #Step -6
    #findcontour(img,contour_retrival_mode,method)
    cnts,hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    try:
        #print("try")
         #Step -7
         # Find contour with maximum area
        cm = max(cnts, key=lambda x: cv2.contourArea(x))
        #print("C==",cnts)
        epsilon = 0.0005*cv2.arcLength(cm,True)
        data= cv2.approxPolyDP(cm,epsilon,True)
    
        hull = cv2.convexHull(cm)
        
        cv2.drawContours(crop_image, [cm], -1, (50, 50, 150), 2)
        cv2.drawContours(crop_image, [hull], -1, (0, 255, 0), 2)
        
        #Step - 8
        # Find convexity defects
        hull = cv2.convexHull(cm, returnPoints=False)
        defects = cv2.convexityDefects(cm, hull)
        count_defects = 0
        #print("Area==",cv2.contourArea(hull) - cv2.contourArea(cm))
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
           
            start = tuple(cm[s][0])
            end = tuple(cm[e][0])
            far = tuple(cm[f][0])
            #Cosin Rule
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = (math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180) / 3.14
            #print(angle)
            # if angle <= 50 draw a circle at the far point
            if angle <= 50:
                count_defects += 1
                cv2.circle(crop_image,far,5,[255,255,255],-1)
        
        print("count==",count_defects)
        
        #Step - 9 
        # Print number of fingers
        if count_defects == 0:
            
            cv2.putText(frame, " ", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255),2)
            print("Pause")
        elif count_defects == 1:
            
            p.press("space")
            cv2.putText(frame, "Play/Pause", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
            print("Play")
        elif count_defects == 2:
            p.press("up")
            
            cv2.putText(frame, "Volume UP", (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
            print("Volume UP")
        elif count_defects == 3:
            p.press("down")
            
            cv2.putText(frame, "Volume Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
            print("Volume Down")
        elif count_defects == 4:
            p.press("right")
            
            cv2.putText(frame, "Forward", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2,(0,0,255), 2)
        else:
            pass
           
    except:
        pass
    #step -10    
    cv2.imshow("Thresh", thresh)
    #cv2.imshow("mask==",mask)
    # cv2.imshow("filter==",filtr)
    cv2.imshow("Result", frame)

    key = cv2.waitKey(25) &0xFF    
    if key == 27: 
        break
cap.release()
cv2.destroyAllWindows()
