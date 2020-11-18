from botocore.exceptions import ClientError
from tinydb import TinyDB, Query
from scipy import stats
from os import path
import numpy as np
import datetime
import logging
import boto3
import time
import sys
import os
"""
def insertCurveAndFeatures(video_path,curve):
    std=np.std(curve)
    variance=std**2
    mean=np.mean(curve)
    median=np.median(curve)
    mode=stats.mode(curve)
    globalmax=max(curve)
    total=sum(curve)
    variancetimegraph=list(curve)
    db = TinyDB('/media/pi/D2D4-2FB6/FrontCamData/AboveThreshold.json')
    print(std,variance,mean,float(mode[0]),median,globalmax,total)
    db.insert({'video_path': video_path,'std': std,'variance':variance,'max':globalmax,'total':total,'mean':mean,'median':median,'mode':float(mode[0]),'curve':variancetimegraph})
"""
def upload_MP4(filepath,bucket_name,object_name,metadata):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(
        filepath,
        bucket_name,
        object_name,
        ExtraArgs={
            "ContentType": "video/mp4",
            "Metadata": metadata,
            "ServerSideEncryption": "AES256"})
    except ClientError as e:
        logging.error(e)
        return False
    return True

def organize_by_date():
	now=datetime.datetime.now()
	t=time.strftime("%I.%M.%S%P")
	DoN=time.strftime("%P")
	y=str(now.year)
	m=str(now.month)
	d=str(now.day)
	metadata={"year": y, "month": m, "day": d, "day_or_night": DoN}
	return y+"/"+m+"/"+d+"/"+DoN+"/"+t+".mp4",metadata
def begin_upload_process(filename,curve):
        if os.path.exists(filename) is True and filename.startswith("/tmp/uploads/temp_Id") is True:
                upload=False
                object_name,metadata=organize_by_date()
                while upload==False and os.path.exists(filename) is True:
                        upload=upload_MP4(filename,'front.cam.storage',object_name,metadata)
                        if upload==True:
                                #insertCurveAndFeatures(object_name,curve)
                                print ('file has been uploaded: ', upload)
                                try:
                                        removed=os.remove(filename)
                                        print ("Successfully removed: ", filename)
                                        break
                                except OSError as error:
                                        print (error)
                                        print ("File path can not be removed")
                                        break
if __name__ == '__main__':
    str(sys.argv)
    """
    curve=[]
    for i in sys.argv[2:]:
        i=float(i)
        curve.append(i)
    print(curve)
    begin_upload_process(str(sys.argv[1]),curve)
    """
    begin_upload_process(str(sys.argv[1]))
