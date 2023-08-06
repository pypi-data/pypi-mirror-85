from pydantic import BaseModel
import uvicorn  
from fastapi import Query,UploadFile,File
from opspipe.app.settings.config import DEBUG
from opspipe.app.main import get_application,get_para
from opspipe.app.core.response.BaseResponse import success, fail
from opspipe.utils import utils
from opspipe.base import logger
app = get_application()
app.description =  '我是API描述'


class Item(BaseModel):  # 创建数据模型,将你的数据模型声明为继承自 BaseModel 的类
    text: str =  Query(  
        '',
        description="我是请求参数",
        deprecated=True 
        )

@app.post("/test",tags=["/test"],
          summary="我是接口描述",
          description='json格式以post方式提交')
async def test(item: Item, ): 
    text = item.dict()['text'] 
    return success(text)


@app.post("/test2")
async def test2(item: str=Query(  
        '',
        description="我是请求参数",
        deprecated=True 
        )): 
    text = item.dict()['text'] 
    return success(text)


@app.post("/test_base64")
async def predict_base64(item: Item):
    #TODO 转换为 文本 
    text = item.dict()['text'] 
    logger.lump_logs('data_file',text) 
    utils.base64_to_file(text,'xxx.txt')
    return success(text)

@app.post("/test_file") 
async def predict_pdf(file: UploadFile = File(...)): 
    pdf_path = utils.save_file(file)
    return success(pdf_path)

if __name__ == '__main__':
    host , port = get_para()
    uvicorn.run(app='__main__:app', host=host, port=port, reload=True, debug=DEBUG)
