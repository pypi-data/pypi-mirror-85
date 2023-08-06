from pydantic import BaseModel
import uvicorn  ,time
from fastapi import Query,UploadFile,File,BackgroundTasks
from opspipe.app.settings.config import DEBUG
from opspipe.app.main import get_application,get_para
from opspipe.app.core.response.BaseResponse import success, fail
from opspipe.utils import utils
from opspipe.base import logger
app = get_application()
app.description =  'test background task'


class Item(BaseModel):  # 创建数据模型,将你的数据模型声明为继承自 BaseModel 的类
    text: str =  Query(  
        '',
        description="我是请求参数",
        deprecated=True 
        )

@app.post("/test",tags=["/test"],
          summary="我是接口描述",
          description='json格式以post方式提交')
async def test(item: Item,  background_tasks: BackgroundTasks): 
    text = item.dict()['text']
    args = background_tasks.is_async
    background_tasks.add_task(test1,text) 
    return success(text)
 
def test1(txt):
    for i in range(1000):
        print(txt)
        time.sleep(5)
        


if __name__ == '__main__':
    host , port = get_para()
    uvicorn.run(app='__main__:app', host=host, port=port, reload=True, debug=DEBUG)
