import cv2
import numpy as np

# capturing the video
cap = cv2.VideoCapture(0)

# geting background as first frame and saving as "background.jpg"
while cap.isOpened():
    isTrue,bg = cap.read()
    cv2.waitKey(1000)
    cv2.imwrite("background.jpg",bg)
    print("background saved!")
    if isTrue:
        break
    
    
#reding background img
loc = "background.jpg"
init_frame = cv2.imread(loc)

# starting the main loop
while cap.isOpened():
    
    # reding camera input 
    isTrue , frame = cap.read()
    
    # converting to hsv
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)   
    
    # defining mask for red colour 
    lower_range = np.array([0,120,70])
    upper_range = np.array([10,255,255]) 
    red_mask = cv2.inRange(hsv_frame,lower_range,upper_range)
    
    # getting too much noice in mask so code getted from web
    red_mask = cv2.morphologyEx(red_mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations=10)
    red_mask = cv2.morphologyEx(red_mask,cv2.MORPH_DILATE,np.ones((3,3),np.uint8), iterations=1)
    
    # inversing the mask
    mask_inv = cv2.bitwise_not(red_mask)
    
    # removing cloath and adding background which is in init_frame
    trans_cloath = cv2.bitwise_and(init_frame,init_frame,mask=red_mask)
    # adding rest of video
    final_frame = cv2.bitwise_and(frame,frame,mask=mask_inv)
    
    # summing final output there
    result = final_frame+trans_cloath

    # showing oringnle picture
    cv2.imshow("orignle",frame)
    
    # invisible cloath output
    cv2.imshow("Invisible Cloath",result)
    
    
    # for braking loop using btn q
    if cv2.waitKey(17)==ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()