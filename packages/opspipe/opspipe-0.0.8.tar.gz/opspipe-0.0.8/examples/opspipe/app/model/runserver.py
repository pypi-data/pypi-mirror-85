#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os, json ,uuid ,fitz, requests 
from fastapi import UploadFile, File,Query
from loguru import logger   
from opspipe.app.core.response.BaseResponse import success, fail 
from opspipe.app.main import get_application, get_para
from opspipe.app.settings.config import DEBUG
from opspipe.base.logger import logtime
from opspipe.utils import utils
from tqdm import tqdm
from pydantic import BaseModel
import uvicorn  

def get_result(text):
    None
    
app = get_application()
app.description =  '建设项目基本情况\n项目批复情况\n项目核准批复文件'  
# -------------------- Business --------------------    
 
'''
# 将PDF转化为图片
pdfPath pdf文件的路径
imgPath 图像要保存的文件夹
zoom_x x方向的缩放系数
zoom_y y方向的缩放系数
rotation_angle 旋转角度
'''
@logtime
def pdf_image(pdfPath,imgPath,zoom_x = 5,zoom_y = 5,rotation_angle = 0):
    # 打开PDF文件
    if not os.path.exists(imgPath):
        os.mkdir(imgPath) 
        
    pdf = fitz.open(pdfPath)
    D = []
    # 逐页读取PDF
    for pg in tqdm(range(0, pdf.pageCount)):
        page = pdf[pg]
        # 设置缩放和旋转系数
        trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotation_angle)
        pm = page.getPixmap(matrix=trans, alpha=False)
        # 开始写图像
        f = os.path.join(imgPath,str(pg)+".png") 
        pm.writePNG(f) 
        D.append(f)
    pdf.close()
    
    return D


@logtime
def ocr(path):
    url = "http://192.168.55.199:30007/icr/recognize_document" 
    files = {'filename': open(path, 'rb')}
    r = requests.post(url, files=files) 
    dt = json.loads(r.text) 
    linesText = dt['linesText']
    return '\n'.join(linesText) ,r.text
 
class Item(BaseModel):
    text: str = Query(
        '',
        description="待抽取文本",
        deprecated=True
    )
 
@app.post("/predict",summary="纯文本抽取接口")
async def predict(item: Item):
    text = item.dict()['text']
    result = get_result(text)
    return success(result)

@app.post("/predict_img", summary="图片抽取文本接口",)
async def predict_img(file: UploadFile = File(...)):  
    img_path = utils.save_file(file)
    try:     
        txt,json = ocr(img_path) 
        rs = {'txt' : txt,
              'result' : json
            }
        logger.info(txt) 
        return success(rs)
    
    except Exception as err: 
        logger.error(f"{err}")
        # TOTO 优化500 全局错误 
        return fail(400)
    
    
@app.post("/predict_pdf", summary="pdf扫描件抽取文本接口") 
async def predict_pdf(file: UploadFile = File(...)):  
    pdf_path = utils.save_file(file)
    try:  
        uid = './' + str(uuid.uuid4()).replace('-','')
        D = pdf_image(pdf_path,uid) 
        txts = []
        rss = []
        for i,img_path in enumerate(D): 
            txt,json = ocr(img_path)
            txts.append(txt) 
            rss.append(json)
            logger.info(str(i) + '/'+ str(len(D)) + '>>>'+ txt)
        rs = {'txt' : ''.join(txts),
              'results' : rss
            }
        return success(rs)
    
    except Exception as err: 
        logger.error(f"{err}")
        # TOTO 优化500 全局错误
        return fail(400)
     
   
if __name__ == '__main__': 
    host , port = get_para()
    uvicorn.run(app='__main__:app', host=host, port=port, reload=True, debug=DEBUG)
