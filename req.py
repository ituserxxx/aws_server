from pydantic import BaseModel, HttpUrl



class AddShopRequest(BaseModel):

    shop_code: str





#
# url = """
# https://www.amazon.com/Headband-Artificial-Hairband-Reversible-Accessories/dp/B0FMNWF5RB/ref=sr_1_1?dib=eyJ2IjoiMSJ9.eveYZvbDhNJW2rE1bzpURSULp61DnAKAae2UMGrIHwTEpSvkfw3RTrlbuwqoLXIFh5b7ShJ7xP64P9VpeufL7NKjA7cRwuze9af_qaLkQmT2eW7-lHAoXiT-S0o8ZZTQsUzEGrswgTU5_FoMArILQsJULxEkUadK9SIv7ugqKVVbzJw_yBnO-OkSX0KEQIFnGZgEJeEquS2jVmmkp7Oc4ppWOXmM-4RqZIFpuH2vpQw.gCT0VbUTsX38asuoLVtankmCQuLwEqgvyfKr2Bi8gOc&dib_tag=se&m=A1RDGTRDC44XWD&qid=1760669109&s=merchant-items&sr=1-1"""
# # 方法1: 使用split分割字符串
# product_id = url.split("/dp/")[1].split("/")[0]
# print(product_id)  # 输出: B0D9GTC2WX


a =  [
    {
        "goods_name": "Retro High Skull Pearl Headband, Vintage High Cranium Artificial Pearl Hairband, Non-Slip Reversible Headband with Teeth Comb for Women Fashion, Hair Accessories Gifts for Girls (3pcs Simple, 1 Set)",
        "dp": "B0FMNWF5RB",
        "goods_detail_url": "https://www.amazon.com/Headband-Artificial-Hairband-Reversible-Accessories/dp/B0FMNWF5RB/ref=sr_1_1?dib=eyJ2IjoiMSJ9.eveYZvbDhNJW2rE1bzpURSULp61DnAKA ... (165 characters truncated) ... eEquS2jVmmkp7Oc4ppWOXmM-4RqZIFpuH2vpQw.eBhr815VUplxVHcJRZkYqwmdwLGaMnbG1N75Fgitfk8&dib_tag=se&m=A1RDGTRDC44XWD&qid=1760683347&s=merchant-items&sr=1_1",
        "goods_img": "https://m.media-amazon.com/images/I/71GM1pD2H7L._AC_UY218_.jpg",
        "shop_code": "A1RDGTRDC44XWD"
    },
    {
        "goods_name": "Mochiinii Thickened Warm Tank Top with Shelf Bra, Cashmere Silk Slim Warm Vest Built in Bra Tank Tops for Women",
        "dp": "B0FWKS94DW",
        "goods_detail_url": "https://www.amazon.com/dp/B0FWKS94DW/ref=sr_1_2?dib=eyJ2IjoiMSJ9.eveYZvbDhNJW2rE1bzpURSULp61DnAKAae2UMGrIHwTEpSvkfw3RTrlbuwqoLXIFh5b7ShJ7xP64P9VpeufL ... (113 characters truncated) ... eEquS2jVmmkp7Oc4ppWOXmM-4RqZIFpuH2vpQw.eBhr815VUplxVHcJRZkYqwmdwLGaMnbG1N75Fgitfk8&dib_tag=se&m=A1RDGTRDC44XWD&qid=1760683347&s=merchant-items&sr=1_2",
        "goods_img": "https://m.media-amazon.com/images/I/61HRBQi7bjL._AC_UY218_.jpg",
        "shop_code": "A1RDGTRDC44XWD"
    }
]
# db = Session()
# try:
#     db.execute(tabModel.insert(), goods_list)
#     db.commit()
# except Exception as e:
#     print(f"Exception scan_shop_goods_list err={str(e)}")
#     db.rollback()
# finally:
#     db.close()