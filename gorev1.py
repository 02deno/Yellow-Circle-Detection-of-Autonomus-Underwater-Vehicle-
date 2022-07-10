import math
import numpy as np
import argparse
import cv2

frameWidth = 640
frameHeight = 480
k = 1
def hareket(x_raw, y_raw, r):

    x_out = 1.5649 * x_raw + 1000
    y_out = 2.0876 * y_raw + 1000
    r_out = 1000 * (r / frameWidth ) + 1000

    har_x = 125 * (math.tanh((3 * x_out / 500 - 9)) + 0.01)*k + 1500
    har_y = -125 * (math.tanh((3 * y_out / 500 - 9)) + 0.01)*k + 1500

    if (r <= ((frameWidth) * 0.69)):
        har_r = -125 * (math.tanh((3 * r_out / 500 - 9)) + 0.01)*k + 1500
    else:
        har_r = 1580
        #time.sleep(10)
    return har_x, har_y, har_r


cap = cv2.VideoCapture(0)
#bilgisayarın kendi kamerasını kullanmak için --> cv2.VideoCapture(0)
#aracın kamerasını kullanmak için --> cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)
counter = 0
while(True):

    ret, captured_frame = cap.read()
    output_frame = captured_frame.copy()

    captured_frame_bgr = cv2.cvtColor(captured_frame, cv2.COLOR_BGRA2BGR)
    captured_frame_bgr = cv2.medianBlur(captured_frame_bgr, 3)
    captured_frame_lab = cv2.cvtColor(captured_frame_bgr, cv2.COLOR_BGR2Lab)

    # Possible yellow threshold: [20, 110, 170][255, 140, 215]
    # Possible blue threshold: [20, 115, 70][255, 145, 120]
    # Possible red threshold : [20, 150, 150][190, 255, 255]
    captured_frame_lab_red = cv2.inRange(captured_frame_lab, np.array([20, 110, 170]), np.array([255, 140, 215]))
    captured_frame_lab_red = cv2.GaussianBlur(captured_frame_lab_red, (5, 5), 2, 2)
    circles = cv2.HoughCircles(captured_frame_lab_red, cv2.HOUGH_GRADIENT, 1, captured_frame_lab_red.shape[0] / 8, param1=60, param2=40, minRadius=25, maxRadius=300)


    
    if circles is not None:
  
        circles = np.round(circles[0, :]).astype("int")
        cv2.circle(output_frame, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(255, 0, 0), thickness=2)
        cv2.rectangle(output_frame, (circles[0, 0] - 5, circles[0, 1] - 5), (circles[0, 0] + 5, circles[0, 1] + 5), (0, 128, 255), -1)

        area = math.pi*circles[0, 0]*circles[0, 0];
        text = "Center is : (" + str(circles[0, 0]) +","+str(circles[0, 1])+") Radius is : "+str(circles[0, 2]) + " Area is : " + str(area)
        #print(text)
        cv2.putText(output_frame,text,(circles[0, 0] - 30, circles[0, 1] - 30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0, 0, 255),2,cv2.LINE_AA)
        print("---------------------------------------")
        print(text)       
        print(hareket(circles[0, 0], circles[0, 1],circles[0, 2]))
        print("---------------------------------------")
        

        
    # Display the resulting frame, quit with q
    cv2.imshow('frame', output_frame)
    cv2.imshow('yellow',captured_frame_lab_red)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
