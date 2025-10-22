import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置Chrome选项
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# 指定WebDriver路径
service = Service('chromedriver-win64/chromedriver.exe')  # 替换为你的chromedriver路径

# 初始化浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)


def init_shop_goods():
    # 找左上角设置站点
    try:
        ck = driver.find_element(
            By.ID, "nav-global-location-slot"
        )
        time.sleep(1)
        ck.click()
        time.sleep(1)
    except Exception as e:
        print(f"1 err={str(e)}")

    try:
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput"))
        )
        time.sleep(1)
        input_element.click()
        time.sleep(1)
        # 步骤 3: 输入 "10010" 到该输入框
        input_element.send_keys("10010")
        time.sleep(1)
    except Exception as e:
        print(f"2 err={str(e)}")

    # 步骤 4: 等待并点击设置的按钮
    try:
        done_button = WebDriverWait(driver, 10).until(
            # EC.element_to_be_clickable((By.ID, "GLUXZipUpdate-announce"))
            EC.element_to_be_clickable((By.XPATH, """//*[@id="GLUXZipUpdate"]/span"""))
        )
        done_button.click()
        # 等待第一个弹窗的元素消失
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="GLUXZipUpdate"]/span'))
        )
        time.sleep(1)
    except Exception as e:
        print(f"3 err={str(e)}")

    try:
        Confirm_button = WebDriverWait(driver, 10).until(
            # EC.element_to_be_clickable((By.ID, "GLUXConfirmClose"))
            EC.element_to_be_clickable((By.XPATH, '//*[contains(@class, "a-popover-footer")]//*[contains(@id, "GLUXConfirmClose")]'))
        )
        time.sleep(1)
        Confirm_button.click()
    except Exception as e:
        print(f"4 err={str(e)}")
    time.sleep(3)


def cont():
    demo_goods_url = "https://www.amazon.com/dp/B0FMTSRKYL"
    driver.get(demo_goods_url)
    # 找continue按钮并点击
    try:
        # 找到按钮并点击
        continue_button = driver.find_element(
            By.XPATH, "/html/body/div/div[1]/div[3]/div/div/form/div/div/span/span/button"
        )
        continue_button.click()
    except Exception as e:
        print("not continue_button")


def god():
    demo_goods_url = "https://www.amazon.com/dp/B0FMTSRKYL"
    driver.get(demo_goods_url)
    # 找商品标题
    try:
        wait = WebDriverWait(driver, 50)
        product_title = wait.until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        ).text
        print(product_title)
    except Exception as e:
        print("not product_title")


def da():
    demo_goods_url = "https://www.amazon.com/dp/B0FMTSRKYL"
    driver.get(demo_goods_url)
    # 找上架日期
    try:
        # 使用 find_elements 获取所有匹配的元素列表
        th_elements = driver.find_elements(By.XPATH, "//th[@class='a-color-secondary a-size-base prodDetSectionEntry']")
        # 获取最后一个 <th> 元素
        last_th = th_elements[-1]
        # 获取对应的 <td> 元素
        last_td = last_th.find_element(By.XPATH, "following-sibling::td").text.strip()
        print(last_td)
    except Exception as e:
        print("not date")


def is_FBA(detail_url):
    # detail_url = "https://www.amazon.com/dp/B0FMTSRKYL" # False
    # detail_url = "https://www.amazon.com/dp/B0FFGLSPPT" # True
    try:
        driver.get("https://www.amazon.com/")
        time.sleep(1)
        driver.get(detail_url)
        return True if driver.find_element(By.ID, "primeDPUpsellStaticContainer") else False
    except Exception as e:
        return False



def shop_goods_list(shop_index_url):
    print(f"shop_index_url: {shop_index_url}")
    # demo_shop_url = "https://www.amazon.com/s?me=A1RDGTRDC44XWD"
    demo_shop_url = "https://www.amazon.com/s?me=A2SSYYG3FPTXOQ"
    demo_shop_url = shop_index_url
    driver.get(demo_shop_url)
    time.sleep(1)
    # sorry 页面
    try:
        if driver.find_element(By.ID, "g"):
            # 出现 sorry 页面就先访问首页
            driver.get("https://www.amazon.com/")
            time.sleep(1)
    except Exception as e:
        print(f"page sorry err={str(e)}")

    driver.get(demo_shop_url)
    time.sleep(1)
    init_shop_goods()

    driver.get(demo_shop_url)

    list_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[@role="listitem" and @data-asin]'))
    )
    goods_list = []
    # 打印所有获取到的 div 元素
    for item in list_items:
        goods_name = None
        goods_img = None
        goods_url = None
        #  商品名称
        try:
            div_element = item.find_element(By.XPATH, './/div[@data-cy="title-recipe"]')
            span_elements = div_element.find_elements(By.XPATH, './/span')
            for span in span_elements:
                goods_name = span.text
                break
        except Exception as e:
            print(f"Exception goods_name  err={str(e)}")
        #  商品首图
        try:
            img_element = item.find_element(By.XPATH, './/img[@class="s-image"]')
            goods_img = img_element.get_attribute('src')
        except Exception as e:
            print(f"Exception goods_img  err={str(e)}")
        #  商品链接
        try:
            goods_ele = item.find_elements(By.XPATH, './/div[@class="aok-relative"]')
            for div in goods_ele:
                a_ele = div.find_elements(By.XPATH, './/a')
                for a in a_ele:
                    goods_url = a.get_attribute('href')  # 获取 href 属性
                    'https://www.amazon.com/Automatic-Interactive-Aggressive-Activated-Rechargeable/dp/B0FBWPNV12'
                    break
                if goods_url:
                    break
        except Exception as e:
            print(f"Exception goods_url  err={str(e)}")

        print({"goods_name": goods_name, "goods_img": goods_img, "goods_url": goods_url})
        goods_list.append({"goods_name": goods_name, "goods_img": goods_img, "goods_url": goods_url})
    return goods_list
# shop_goods_list()
# time.sleep(222)

# 关闭浏览器
# driver.quit()


