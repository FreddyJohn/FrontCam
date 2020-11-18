from botocore.exceptions import ClientError
from imutils.video import VideoStream
from subprocess import Popen, PIPE
import multiprocessing as mp
import numpy as np
import datetime
import random
import psutil
import boto3
import time
import cv2
import os
def getVoSD (frame,last_frame):
    current_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    difference = (cv2.absdiff(current_frame, last_frame))
    differences = np.hsplit(difference,1)
    differences = np.vsplit(differences[0],[70,640])
    variance = np.std(differences[1])
    return variance
def graphics(frame,time_stamp,graph,font):
    cv2.rectangle(frame, (0,0),(404,35), (0,0,0),-1)
    cv2.rectangle(frame, (404,0),(640,35), (0,0,0),-1)
    cv2.putText(frame, time_stamp, (1,25), font, .80, (0,255,0), 5, cv2.LINE_AA)
    cv2.polylines(frame,graph,True, (0,255,0),2)
    cv2.rectangle(frame, (404,0),(640,33), (50,50,50),4)
    return frame
def CameraOn():
    os.system('mkdir /tmp/uploads')
    xvals = np.arange(405,641,1)
    yvals = np.ones(236)*30
    graph=(np.r_['1,2,0',xvals,yvals]).astype(int).reshape(-1,1,2)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    font = cv2.FONT_HERSHEY_SIMPLEX
    video_name = 'SecurityFeed'
    cap = cv2.VideoCapture(0)
    pool=mp.Pool(4)
    scope = 0
    while cap.isOpened():
        variance_values=[]
        variance=0.0
        movement=False
        timetrack=0.0
        timeup=False
        newname=str(time.time()).replace('.',str(random.randint(256,1024)))
        os.system('sudo find /tmp/uploads -type f -cmin +10 -delete')
        move_file='/tmp/uploads/temp_Id'+newname+'.mp4'
        moveout = cv2.VideoWriter(move_file, fourcc, 10.0, (640,480),True)
        while cap.isOpened():
            ret,frame = cap.read()
            movementframe=frame
            display=cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            time_stamp=str(datetime.datetime.now())
            cv2.namedWindow(video_name, cv2.WND_PROP_AUTOSIZE)
            cv2.setWindowProperty(video_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            display=graphics(display,time_stamp,graph,font)
            cv2.imshow(video_name,display)
            if frame is not None and scope==1:
               variance=pool.apply(getVoSD, args=(frame,last_frame))
               yvals=np.roll(yvals,1)
               yvals[0]=31-variance
               graph=(np.r_['1,2,0',xvals,yvals]).astype(int).reshape(-1,1,2)
               scope-=1
               #variance_values.append(variance)
               #print (variance)
               if variance>=4.5:
                   variance_values.append(variance)
                   timetrack=time.perf_counter()
                   movement=True
            last_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if last_frame is not None:
                scope+=1
            if time.perf_counter()-timetrack>=12 and movement == True:
                moveout.release()
                timeup=True
            elif movement == True:
                movementframe=graphics(movementframe,time_stamp,graph,font)
                moveout.write(movementframe)
                cv2.imshow(video_name,movementframe)
            if timeup==True:
                try:
                   process=Popen(['python3','AWSauto.py',move_file]+[str(i) for i in variance_values])
                except OSError:
                   process=Popen(['python3','AWSauto.py',move_file])
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
if __name__ == '__main__':
    print ('I will now look for movement')
    CameraOn()
else:
    print ("this is not a python library")
