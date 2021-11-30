#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 19:33:54 2021

@author: caojiajia
"""


'''
--------------------------------------------------------------------------------------------------
使用相機擷取車牌資訊與儲存影像（自己測試時這段不要跑除非你能把車牌搬到電腦前ＸＤ）
--------------------------------------------------------------------------------------------------
'''
import boto3
import cv2
import time
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor

#擷取車牌影像(開啟相機)

cap = cv2.VideoCapture(0)

milli = int(round(time.time() * 1000))

while(True):
    

  milli = 2*1000
  cv2.waitKey(milli)
  
  time.sleep(3) ##延遲執行的秒數:3
  
  ret, frame = cap.read()  #捕獲一幀影象
  cv2.imshow('frame', frame)  #顯示影像
  cv2.imwrite('Car.png',frame, [int( cv2.IMWRITE_PNG_QUALITY), 95]) #儲存影像（png）
  
  break


cap.release()  #關閉相機
cv2.destroyAllWindows()  #關閉視窗


'''
--------------------------------------------------------------------------------------------------
新建Database
--------------------------------------------------------------------------------------------------
'''
import csv
def readimage():
    file = '/Users/caojiajia/Desktop/python/習題存檔/AWS_Rekognition專案/CarLicense.csv'
    with open(file,'r') as csvfile:
        rows = csv.reader(csvfile)
        CarLicense = [data for data in rows]
    License = {CarLicense[number][0] : number for number in range(1,4)}
    
    HouseNumber = {CarLicense[number][1]:number for number in range(1,4)}
    
    return CarLicense,License,HouseNumber

CarLicense,License,HouseNumber = readimage()

'''
--------------------------------------------------------------------------------------------------
讀取車牌影像檔案
--------------------------------------------------------------------------------------------------
'''
imgfilename = '/Users/caojiajia/Desktop/python/習題存檔/AWS_Rekognition專案/Car.png'
with open(imgfilename,'rb') as imgfile:
    imgbytes = imgfile.read()

'''
--------------------------------------------------------------------------------------------------
AWS帳號－－連結用金鑰儲存 (請大家改自己的金鑰)
--------------------------------------------------------------------------------------------------
'''
ACCESS_KEY = 'AKIA4PVPUCZPCEXZCFGJ'
SECRET_KEY = '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'

'''
--------------------------------------------------------------------------------------------------
上傳AWS 
--------------------------------------------------------------------------------------------------
'''

def detect_labels():
   
    with open('/Users/caojiajia/Desktop/python/習題存檔/AWS_Rekognition專案/new_user_credentials.csv','r') as input:
        next(input)
        reader = csv.reader(input)
        for line in reader:
            access_key_id = line[2]
            secret_access_key = line[3]

     
    client=boto3.client('rekognition',region_name='us-east-1',
                        aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)
    
    response = client.detect_text(Image={'Bytes': imgbytes})  #選取AWS上分析出所需資訊
    textDetect = response['TextDetections']
    
    textSet = set()    #分析出的資料存在textSet裏面（目前空）
    for index in range(len(textDetect)):
        if textDetect[index]['DetectedText']:
            textSet.add(textDetect[index]['DetectedText']) #將textDetect的部分加進textSet
    
    return textDetect,textSet

textDetect, selectedText = detect_labels()

'''
-----------------------------------------------------------------------------------------------
比對資料階段 0901通關！！！
-----------------------------------------------------------------------------------------------
'''


textSet_list = list(textSet)
textSet_str = str(textSet)
License_str = str(License)

License_list = list(License_str)
textSet_srt = sorted(textSet_list, key=len , reverse=True) #根據字串由大到小排序 我只要大的！（車牌號碼）
#print(textSet_srt)   ['EAA-5555', '5']


def analyze():
    for textSet_list in selectedText:
        print('歡迎回來,車牌： ' , textSet_srt[0])
        break
    else:
        print('車牌尚未登記,請至管理室由專人處理')
analyze()
#歡迎回來,車牌：  EAA-5555
