"""
路由
""" 
from fastapi import APIRouter
from fastapi.responses import HTMLResponse 
from ...settings import config 
from starlette.responses import RedirectResponse  
router = APIRouter()

@router.get("/", summary="首页", include_in_schema=False)
async def root():
    return RedirectResponse('/docs')


@router.get(config.MDDOC_URL, summary="生成 .MD 接口文档", response_class=HTMLResponse)
async def mddoc():   
    with open(config.MDDOC_DIR, 'r', encoding='utf-8') as f: 
        mddoc = f.read()
        return mddoc
