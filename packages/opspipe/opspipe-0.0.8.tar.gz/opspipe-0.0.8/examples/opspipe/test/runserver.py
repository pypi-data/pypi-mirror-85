#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os, json,requests 
import uvicorn  
from opspipe.app.settings.config import DEBUG
from opspipe.app.main import get_application,get_para
from opspipe.app.core.response.BaseResponse import success, fail 
from fastapi import Query  
from loguru import logger   
from pydantic import BaseModel
from fastapi import UploadFile, File
from opspipe.base.logger import logtime
from opspipe.utils import utils
from construction_enterprise_qualification_certificate import get_result
# -------------------- System --------------------   
app = get_application()
app.description =  '建筑业企业资质证书识别'
 
 
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
 

@app.post("/predict_img", summary="图片抽取接口",)
async def predict_img(file: UploadFile = File(...)):  
    img_path = utils.save_file(file)
    try:     
        txt,json = ocr(img_path) 
        print(txt)
        result = get_result(txt) 
        return success(result)
    
    except Exception as err: 
        logger.error(f"{err}")
        # TOTO 优化500 全局错误 
        return fail(400)
    
@app.post("/predict",summary="纯文本抽取接口")
async def predict(item: Item):
    text = item.dict()['text']
    result = get_result(text)
    return success(result)
  
     
if __name__ == '__main__':
    host , port = get_para()
    uvicorn.run(app='__main__:app', host=host, port=port, reload=True, debug=DEBUG)
