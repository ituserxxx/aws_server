import logging
import threading
import time
from datetime import datetime, timedelta

import schedule
from sqlalchemy import create_engine, Column, Integer, String, Text, text, MetaData, Table, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import shop
from dotenv import load_dotenv

load_dotenv()
# 配置日志，设置日志级别为 ERROR，只显示错误日志
logging.basicConfig(level=logging.ERROR)

# 创建数据库引擎
engine = create_engine(os.getenv("mysql_conn", "mysql_database_url_errrrrrr"), echo=True)

# 创建基类
Base = declarative_base()

# 创建 Session 类

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)  # 线程安全会话工厂


# 定义模型
class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_index_url = Column(Text, nullable=True)
    shop_code = Column(String(255), nullable=True)

    def to_json(self):
        return {'id': self.id, 'shop_index_url': self.shop_index_url, 'shop_code': self.shop_code}


# 动态指定表名


def get_dynamic_table(date_suffix):
    metadata = MetaData()
    table_name = f"goods_{date_suffix}"
    return Table(table_name, metadata,
                 Column('id', Integer, primary_key=True),
                 Column('goods_name', String(255), nullable=False),
                 Column('dp', String(255), nullable=False),
                 Column('goods_detail_url', String(255), nullable=False),
                 Column('goods_img', String(255), nullable=False),
                 Column('shop_code', String(255), nullable=True),
                 Column('is_new', Integer, nullable=True)
                 )


# 定义创建表的函数
def job_create_table():
    try:
        # 获取今天的日期
        today_date = datetime.now().strftime('%Y_%m_%d')
        sql = f"""
            CREATE TABLE  IF NOT EXISTS `goods_{today_date}` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `goods_name` text COLLATE utf8_unicode_ci,
              `goods_detail_url` text COLLATE utf8_unicode_ci,
               `dp` text COLLATE utf8_unicode_ci,
              `goods_img` text COLLATE utf8_unicode_ci,
              `shop_code` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
              `is_new` tinyint(1) DEFAULT '0',
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='{today_date}的商品表';  
            """

        with Session() as conn:
            conn.execute(text(sql))
            conn.commit()

        yester_date = pre_date(today_date)
        sql2 = f"""
                    CREATE TABLE  IF NOT EXISTS `goods_{yester_date}` (
                      `id` int(11) NOT NULL AUTO_INCREMENT,
                      `goods_name` text COLLATE utf8_unicode_ci,
                      `goods_detail_url` text COLLATE utf8_unicode_ci,
                       `dp` text COLLATE utf8_unicode_ci,
                      `goods_img` text COLLATE utf8_unicode_ci,
                      `shop_code` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
                       `is_new` tinyint(1) DEFAULT '0',
                      PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='{yester_date}的商品表';  
                    """

        with Session() as conn:
            conn.execute(text(sql2))
            conn.commit()
    except Exception as e:
        print(f"job_create_table Exception err={str(e)}")
    finally:
        # schedule.cancel_job(schedule.get_jobs()[0])
        pass


def pre_date(d):
    # 将字符串转换为datetime对象
    date_obj = datetime.strptime(d, '%Y_%m_%d')
    # 计算前一天
    previous_day = date_obj - timedelta(days=1)
    # 格式化输出
    return previous_day.strftime('%Y_%m_%d')


def scan_shop_goods_list(shop_index_url, shop_code):
    today_date = datetime.now().strftime('%Y_%m_%d')
    yester_date = pre_date(today_date)
    print(f"后台任务开始运行...{shop_index_url}")
    shop_chrom = shop.Shop(shop_index_url=shop_index_url)
    goods_list = shop_chrom.get_shop_goods_list(shop_code,today_date)
    shop_chrom.quite_drive()

    del shop_chrom
    if len(goods_list) > 0:
        todayModel = get_dynamic_table(today_date)
        yesterModel = get_dynamic_table(yester_date)
        db = Session()
        try:
            for goods in goods_list:
                if goods['dp']:
                    # 检查商品在昨天的表中是否已存在
                    is_exist = db.query(
                        # B0CYZM5RSM
                        exists().where(yesterModel.c.dp == goods['dp']
                                       # yesterModel.c.is_new == '1'
                                       )
                    ).scalar()
                    if is_exist:
                        goods['is_new'] = 0
                    else:
                        goods['is_new'] = 1
                    db.execute(todayModel.insert(), goods)
            db.commit()
        except Exception as e:
            print(f"Exception scan_shop_goods_list err={str(e)}")
            db.rollback()
        finally:
            db.close()


def job_scan_shop_task():
    db = None
    try:
        db = Session()
        #  ["https://www.amazon.com/s?me=A1RDGTRDC44XWD", "https://www.amazon.com/s?me=A2SSYYG3FPTXOQ"]
        shop_list = db.query(Shop).all()
        for shopItem in shop_list:
            # threading.Thread(target=scan_shop_goods_list, args=(shopItem.shop_index_url, shopItem.shop_code), daemon=True).start()  # 在后台线程中运行任务
            scan_shop_goods_list(shopItem.shop_index_url, shopItem.shop_code)
    except Exception as e:
        print(f"job_scan_shop_task Exception err={str(e)}")
        db.rollback() if db else None
    finally:
        db.close() if db else None
        # schedule.cancel_job(schedule.get_jobs()[0])


def schedule_task():
    # 使用 schedule 每天凌晨 1 点执行任务
    schedule.every().day.at("00:10").do(job_create_table)
    schedule.every().day.at("00:14").do(job_scan_shop_task)
    # 立即执行任务（仅一次）
    if os.getenv("schedule_once", 'no') == 'yes':
        schedule.run_all()  # 立即执行所有已调度的任务
    while True:
        schedule.run_pending()  # 运行待定的任务
        time.sleep(1)  # 每秒检查一次任务是否到时间

#
# a =  [
#     {
#         "goods_name": "Retro High Skull Pearl Headband, Vintage High Cranium Artificial Pearl Hairband, Non-Slip Reversible Headband with Teeth Comb for Women Fashion, Hair Accessories Gifts for Girls (3pcs Simple, 1 Set)",
#         "dp": "B0FMNWF5RB",
#         "goods_detail_url": "https://www.amazon.com/Headband-Artificial-Hairband-Reversible-Accessories/dp/B0FMNWF5RB/ref=sr_1_1?dib=eyJ2IjoiMSJ9.eveYZvbDhNJW2rE1bzpURSULp61DnAKA ... (165 characters truncated) ... eEquS2jVmmkp7Oc4ppWOXmM-4RqZIFpuH2vpQw.eBhr815VUplxVHcJRZkYqwmdwLGaMnbG1N75Fgitfk8&dib_tag=se&m=A1RDGTRDC44XWD&qid=1760683347&s=merchant-items&sr=1_1",
#         "goods_img": "https://m.media-amazon.com/images/I/71GM1pD2H7L._AC_UY218_.jpg",
#         "shop_code": "A1RDGTRDC44XWD"
#     },
#     {
#         "goods_name": "Mochiinii Thickened Warm Tank Top with Shelf Bra, Cashmere Silk Slim Warm Vest Built in Bra Tank Tops for Women",
#         "dp": "B0FWKS94DW",
#         "goods_detail_url": "https://www.amazon.com/dp/B0FWKS94DW/ref=sr_1_2?dib=eyJ2IjoiMSJ9.eveYZvbDhNJW2rE1bzpURSULp61DnAKAae2UMGrIHwTEpSvkfw3RTrlbuwqoLXIFh5b7ShJ7xP64P9VpeufL ... (113 characters truncated) ... eEquS2jVmmkp7Oc4ppWOXmM-4RqZIFpuH2vpQw.eBhr815VUplxVHcJRZkYqwmdwLGaMnbG1N75Fgitfk8&dib_tag=se&m=A1RDGTRDC44XWD&qid=1760683347&s=merchant-items&sr=1_2",
#         "goods_img": "https://m.media-amazon.com/images/I/61HRBQi7bjL._AC_UY218_.jpg",
#         "shop_code": "A1RDGTRDC44XWD"
#     }
# ]
# db = Session()
# try:
#     today_date = datetime.now().strftime('%Y_%m_%d')
#     tabModel = get_dynamic_table(today_date)
#     db.execute(tabModel.insert(), a)
#     db.commit()
# except Exception as e:
#     print(f"Exception scan_shop_goods_list err={str(e)}")
#     db.rollback()
# finally:
#     db.close()

#
# db = Session()
# try:
#     today_date = datetime.now().strftime('%Y_%m_%d')
#     yesterModel = get_dynamic_table(today_date)
#
#     # 检查商品在昨天的表中是否已存在
#     is_exist = db.query(
#         # B0CYZM5RSM
#         exists().where(
#             yesterModel.c.dp == 'B0CYZM5RSM',
#             yesterModel.c.is_new == '1')
#     ).scalar()
#     if is_exist:
#         print(111)
#     else:
#         print(0)
#     # db.commit()
# except Exception as e:
#     print(f"Exception scan_shop_goods_list err={str(e)}")
#     db.rollback()
# finally:
#     db.close()
