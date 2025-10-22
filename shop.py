import os
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from dotenv import load_dotenv

load_dotenv()
"""
https://www.amazon.com/Keurig-Compact-Portable-Machine-Offices/dp/B0FMTSRKYL/ref=zg_bsnr_c_home-garden_d_sccl_1/132-2598300-5858640?pd_rd_w=v4ykz&content-id=amzn1.sym.fef9af56-6177-46e9-8710-a5293a68dd39&pf_rd_p=fef9af56-6177-46e9-8710-a5293a68dd39&pf_rd_r=QCTVGEQ79N2PQPK2PRDM&pd_rd_wg=YrKwL&pd_rd_r=9b7cee08-fc4a-43f0-9090-90e470e2d9a4&pd_rd_i=B0FMTSRKYL&th=1
INSERT INTO `aws_shop`.`shops` (`id`, `shop_index_url`, `shop_code`) VALUES (1, 'https://www.amazon.com/s?me=A1RDGTRDC44XWD', 'A1RDGTRDC44XWD');
INSERT INTO `aws_shop`.`shops` (`id`, `shop_index_url`, `shop_code`) VALUES (2, 'https://www.amazon.com/s?me=A2SSYYG3FPTXOQ', 'A2SSYYG3FPTXOQ');

"""


class Shop(object):
    def __init__(self, shop_index_url):
        self.driver = None
        self.shop_index_url = shop_index_url
        self._set_chrome()

    def quite_drive(self):
        self.driver.quit()

    def _set_chrome(self):
        # 设置Chrome选项
        chrome_options = Options()
        if os.getenv("is_headless", False) == 'yes':
            chrome_options.add_argument("--headless")  # 无头模式
        if os.getenv("is_pro", "no") == 'yes':
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        """
        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36
        Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3.1 Mobile/15E148 Safari/604.1
        """
        # 随机User-Agent配置

        ua = UserAgent(os='windows',
                       browsers=['chrome'],
                       min_percentage=5,  # 过滤市占率低于5%的版本
                       # exclude=['mobile']
                       )  # 排除移动设备)  # 限定Windows平台
        win_chrome_ua = ua.chrome  # 明确调用chrome生成器
        print(f"agent={win_chrome_ua}")

        chrome_options.add_argument(f"user-agent={win_chrome_ua}")

        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument("--blink-settings=imagesEnabled=false")

        # 指定WebDriver路径
        service = Service(os.getenv("chromedriver_path", "chromedriver_path_errrrrrr"))  #
        # 初始化浏览器
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            # "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0"
            "userAgent": ua.chrome
        })
        self.driver = driver

    def _init_shop_goods(self):
        # 找左上角设置站点
        try:
            ck = self.driver.find_element(
                By.ID, "nav-global-location-slot"
            )
            time.sleep(1)
            ck.click()
            time.sleep(1)
        except Exception as e:
            print(f"_init_shop_goods Exception 1 err={str(e)}")

        try:
            input_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput"))
            )
            time.sleep(1)
            input_element.click()
            time.sleep(1)
            # 步骤 3: 输入 "10010" 到该输入框
            input_element.send_keys("10001")
            time.sleep(1)
        except Exception as e:
            print(f"_init_shop_goods Exception  2 send_keys err={str(e)}")

        # 步骤 4: 等待并点击设置的按钮
        try:
            done_button = WebDriverWait(self.driver, 10).until(
                # EC.element_to_be_clickable((By.ID, "GLUXZipUpdate-announce"))
                EC.element_to_be_clickable((By.XPATH, """//*[@id="GLUXZipUpdate"]/span"""))
            )
            done_button.click()
            # 等待第一个弹窗的元素消失
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '//*[@id="GLUXZipUpdate"]/span'))
            )
            time.sleep(1)
        except Exception as e:
            print(f"_init_shop_goods Exception   3 done_button err={str(e)}")

        try:
            Confirm_button = WebDriverWait(self.driver, 10).until(
                # EC.element_to_be_clickable((By.ID, "GLUXConfirmClose"))
                EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "a-popover-footer")]//*[contains(@id, "GLUXConfirmClose")]'))
            )
            time.sleep(1)
            Confirm_button.click()
        except Exception as e:
            print(f"_init_shop_goods Exception   4 Confirm_button err= ")
        time.sleep(3)

    def check_sorry_page(self):
        self.random_delay()
        # sorry 页面
        try:
            if self.driver.find_element(By.ID, "g"):
                # 出现 sorry 页面就先访问首页
                # self.driver.get("https://www.amazon.com/")
                self.driver.get(self.shop_index_url)
                self.random_delay()

            continue_button = self.driver.find_element(By.XPATH, "//button[@class='a-button-text']")
            if continue_button:
                continue_button.click()
                time.sleep(1)
        except Exception as e:
            print(f"page sorry err= ")

    def get_shop_goods_list(self, shop_code, today_date):
        # demo_shop_url = "https://www.amazon.com/s?me=A1RDGTRDC44XWD"
        # demo_shop_url = "https://www.amazon.com/s?me=A2SSYYG3FPTXOQ"
        self.driver.get(self.shop_index_url)
        self._init_shop_goods()
        goods_list = []
        page_size = 16
        page_num = 0
        is_end = False
        while not is_end:
            self.random_delay()
            try:
                if page_num == 0:
                    self.driver.get(self.shop_index_url)
                    self.check_sorry_page()
                page_items = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem" and @data-asin]'))
                )
                page_size = len(page_items)
                print(f"page_num={page_num}, page_size={page_size}")
                if page_size > 0:
                    goods_list.extend(self.get_goods_info(page_items, shop_code))
                if page_size < 16:
                    is_end = True
                    goods_list.extend(self.get_goods_info(page_items, shop_code))
                    continue
                time.sleep(random.randint(1, 5))
            except Exception as e:
                print(f"get_shop_goods_list page not is_not_listitem err={str(e)}")
            if page_size == 16:
                try:
                    # 等待并定位最后一个<li>元素
                    next_page = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//ul[@class='a-unordered-list a-horizontal s-unordered-list-accessibility']/li[last()]"))
                    )
                    if next_page:
                        # 确保元素可点击后点击
                        WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//ul[@class='a-unordered-list a-horizontal s-unordered-list-accessibility']/li[last()]"))
                        ).click()
                        page_num += 1
                except Exception as e:
                    print(f"get_shop_goods_list next_page err={str(e)}")

        print(f"shop_code={shop_code} today_date={today_date} 获取到商品数量 {len(goods_list)}")

        # return []
        return self.get_shop_fbm_goods(goods_list, shop_code)

    def get_goods_info(self, page_items, shop_code):
        goods_list = []
        # 打印所有获取到的 div 元素
        for item in page_items:
            self.random_delay()
            goods_name = None
            dp = None
            goods_img = None
            goods_detail_url = None

            #  商品名称
            try:
                div_element = item.find_element(By.XPATH, './/div[@data-cy="title-recipe"]')
                span_elements = div_element.find_elements(By.XPATH, './/span')
                for span in span_elements:
                    goods_name = span.text
                    break
            except Exception as e:
                print(f"get_shop_all_goods shop_code={shop_code} Exception goods_name  err={str(e)}")
            #  商品首图
            try:
                img_element = item.find_element(By.XPATH, './/img[@class="s-image"]')
                goods_img = img_element.get_attribute('src')
            except Exception as e:
                print(f"get_shop_all_goods shop_code={shop_code}  Exception goods_img  err={str(e)}")
            #  商品链接
            try:
                a_elements = item.find_elements(By.XPATH, './/a[@class="a-link-normal s-line-clamp-2 s-link-style a-text-normal"]')
                # div_element = item.find_element(By.XPATH, './/div[@data-cy="title-recipe"]')
                # a_elements = div_element.find_elements(By.XPATH, './/a')
                for a in a_elements:
                    goods_detail_url = a.get_attribute('href')  # 获取 href 属性
                    break
                if goods_detail_url:
                    try:
                        dp = goods_detail_url.split("/dp/")[1].split("/")[0]
                    except Exception as e:
                        print(f"get_shop_all_goods shop_code={shop_code}  Exception dp  err={str(e)}")
                    # break
            except Exception as e:
                print(f"get_shop_all_goods shop_code={shop_code}  Exception goods_url1  err={str(e)}")
                try:
                    div_element = item.find_element(By.XPATH, './/div[@data-cy="title-recipe"]')
                    a_elements = div_element.find_elements(By.XPATH, './/a')
                    for a in a_elements:
                        goods_detail_url = a.get_attribute('href')  # 获取 href 属性
                        break
                    if goods_detail_url:
                        try:
                            dp = goods_detail_url.split("/dp/")[1].split("/")[0]
                        except Exception as e:
                            print(f"get_shop_all_goods shop_code={shop_code}  Exception dp  err={str(e)}")
                except Exception as e:
                    print(f"get_shop_all_goods shop_code={shop_code}  Exception goods_url2  err={str(e)}")
            goods_list.append({
                "goods_name": goods_name,
                "goods_img": goods_img,
                "goods_detail_url": goods_detail_url,
                "dp": dp,
                "shop_code": shop_code,
            })

        return goods_list

    def get_shop_fbm_goods(self, goods_list, shop_code):
        add_goods_list = []
        for item in goods_list:
            self.random_delay()
            # 判断是否是 FBA
            is_fba = False
            try:
                if item['goods_detail_url'] is not None:
                    self.driver.get(item['goods_detail_url'])  # 这里其实是去判断 fba，如果是 fab 则跳过
                    div_fba = self.driver.find_element(By.ID, "primeDPUpsellStaticContainer")
                    inner_html = div_fba.get_attribute("innerHTML")
                    if inner_html.strip():  # 检查innerHTML是否为空
                        is_fba = True
            except Exception as e:
                print(f"get_shop_all_goods shop_code={shop_code} Exception   is_fba1 err= ")
                try:
                    div_fba2 = self.driver.find_element(By.ID, "primeDPUpsellStaticContainerNPA")
                    inner_html2 = div_fba2.get_attribute("innerHTML")
                    if inner_html2.strip():  # 检查innerHTML是否为空
                        # print("元素包含子元素或文本内容")
                        is_fba = True
                    # else:
                    #     print("元素为空")
                except Exception as e:
                    print(f"get_shop_all_goods shop_code={shop_code} Exception   is_fba2 err= ")
                    continue
            if is_fba:
                continue
            add_goods_list.append(item)
        print(f" 店铺{shop_code}FBM数量{len(add_goods_list)}")
        return add_goods_list

    def random_delay(self, min_sec=1, max_sec=3):
        time.sleep(random.uniform(min_sec, max_sec))
