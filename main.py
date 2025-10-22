import threading
import time
import signal
import sys
from typing import Union
from datetime import datetime
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from starlette.responses import FileResponse

import model
import req
from fastapi.staticfiles import StaticFiles

load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/web", StaticFiles(directory="web/assets"), name="web")
# 必须保留根路由指向首页
@app.get("/")
async def serve_index():
    return FileResponse("web/index.html")

# 处理前端路由（如Vue Router的history模式）
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return FileResponse("web/index.html")

@app.on_event("startup")
def start_background_task():
    threading.Thread(target=model.schedule_task, daemon=True).start()


@app.post("/api/shops_list")
async def shop_list():
    db = None
    try:
        db = model.Session()
        # 查询所有数据
        results = db.query(model.Shop).all()
        result_dict = [row.to_json() for row in results]
        return {
            "code": 0,
            "data": result_dict
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            "code": -1,
            "data": str(e)
        }
    finally:
        db.close() if db else None



@app.post("/api/add_shop")
async def add_shop(params: req.AddShopRequest):
    db = None
    try:
        db = model.Session()
        # 查询所有数据
        new_record = model.Shop(shop_index_url=f"https://www.amazon.com/s?me={params.shop_code}", shop_code=params.shop_code)
        db.add(new_record)
        db.flush()
        db.commit()
        return {
            "code": 0,
            "data": new_record.id
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            "code": -1,
            "data": str(e)
        }
    finally:
        db.close() if db else None


@app.post("/api/goods_list",)
async def goods_list():
    db = None
    try:
        today_date = datetime.now().strftime('%Y_%m_%d')
        tabModel = model.get_dynamic_table(today_date)
        db = model.Session()
        # 查询所有数据
        results = db.query(tabModel).filter(tabModel.c.is_new==1).all()
        result_dict = [dict(zip([column.name for column in tabModel.columns], row)) for row in results]
        return {
            "code": 0,
            "data": result_dict
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            "code": -1,
            "data": str(e)
        }
    finally:
        db.close() if db else None


# 捕获 SIGINT 信号（Ctrl+C），在关闭应用时优雅地终止线程
def signal_handler(sig, frame):
    sys.exit(0)  # 优雅退出


# 注册信号处理器
signal.signal(signal.SIGINT, signal_handler)
