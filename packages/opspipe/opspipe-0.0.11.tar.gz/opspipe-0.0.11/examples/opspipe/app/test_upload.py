# -*- coding: utf-8 -*-
'''
Created on 2020-11-6

@author: zhys513(254851907@qq.com)
'''
import requests,json
''' OCR
url = "http://192.168.55.199:30007/icr/recognize_document"
path = "C:\\Users\\Administrator\\Desktop\\train\\images\\images0.png"
files = {'filename': open(path, 'rb')}
r = requests.post(url, files=files)
print(r.url)
print(r.text)
txt = r.text
dt = json.loads(txt) 

linesText = dt['linesText']
print(linesText)
'''


url = "http://192.168.49.138:8080/converTxt" 
files = {'file': open('C:\\Users\\Administrator\\Desktop\\opspipe-0.0.3\\1.ceb', 'rb')}
r = requests.post(url, files=files) 
dt = json.loads(r.text) 
print(dt)
linesText = dt['content'] 