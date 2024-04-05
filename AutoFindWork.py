# articleReWriter.py
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from openpyxl import Workbook
import time, threading, os
import configparser
import pandas as pd

# 创建互斥锁
lock = threading.Lock()


class SingleBossOffer:
    def __init__(self, name, tags, salary):
        self.name = name
        self.tags = tags
        self.salary = salary

class SingleOffer:
    def __init__(self, name, company):
        self.name = name
        self.company = company

class BossOffer:
    def __init__(self, name, tags, salary, company, el, tagsEl):
        self.name = name
        self.tags = tags
        self.salary = salary
        self.company = company
        self.address = ""
        self.el = el
        self.tagsEl = tagsEl

        # 定义对象的字符串表示
    def __str__(self):
        return f"BossOffer(name={self.name}, tags={self.tags}" \
               f", salary={self.salary}, company={self.company}" \
               f", address={self.address})"

    # 定义对象的正式字符串表示
    def __repr__(self):
        return f"BossOffer(name={self.name!r}, tags={self.tags}" \
               f", salary={self.salary}, company={self.company}" \
               f", address={self.address})"

    def getSingle(self):
        return SingleBossOffer(self.name, self.tags, self.salary)


def saveExcel(offers=[], excelFile='hasApplyOffer.xlsx'):
    old_df = pd.read_excel(excelFile, sheet_name='Sheet1', engine='openpyxl')
    # 将对象列表转换为DataFrame
    df = pd.DataFrame([{'Name': p.name, 'Salary': p.salary, 'Company': p.company, 'Address': p.address, 'Tags': p.tags} for p in offers])
    combined_df = pd.concat([old_df, df], ignore_index=True)
    # 保存DataFrame为Excel文件
    combined_df.to_excel(excelFile, index=False)


def getHasApplyOffersByExcel(excelFile='hasApplyOffer.xlsx'):
    hasApplyOffers=[]
    if not os.path.exists(excelFile):
        # 文件不存在，创建一个Excel工作簿
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"  # 设置工作表标题
        # 保存工作簿到文件
        wb.save(excelFile)
        print(f'文件 {excelFile} 已创建')
        return hasApplyOffers
    # 读取Excel文件
    df = pd.read_excel(excelFile, sheet_name='Sheet1', engine='openpyxl')
    for index, row in df.iterrows():
        # 创建Person实例并添加到列表中
        o = SingleOffer(row['Name'], row['Company'])
        hasApplyOffers.append(o)
    return hasApplyOffers


def isContainer(acquireTags, tags):
    for a in acquireTags:
        if a in tags:
            return True
    return False


def getStr(encoded_str):
    mapping = {
        "": "0",
        "": "1",
        "": "2",
        "": "3",
        "": "4",
        "": "5",
        "": "6",
        "": "7",
        "": "8",
        "": "9",
        "K": "K",
        "-": "-",
        "·": "·",
        "薪": "薪"
    }
    # 使用映射关系解码字符串
    decoded_str = ''.join(mapping[char] for char in encoded_str)
    return decoded_str


def isComfortable(name, tags, salary, keywordLst=[], lifeTags=[]):
    res = isContainer(lifeTags, tags) and (int)(salary.split("-")[0]) >= 8
    hasKeywords = False;
    for k in keywordLst:
        hasKeywords = hasKeywords or str.lower(k) in str.lower(name)
    res = hasKeywords and res;
    return res


def sendResumeByKeyword(keywordLst=[], acquiretags=[], addressTags=[], whileCount=3, isNew=False):
    # 获取锁
    lock.acquire()
    try:
        # 创建ConfigParser对象
        config = configparser.ConfigParser()
        driver = connectCurrentChrome()
        tmp = 0
        if isNew:
            config.read('config.ini')
            config.set('default', 'index', '1')
        while tmp < whileCount:
            config.read('config.ini')
            # 获取temp_value的值
            index = config.getint('default', 'index')
            element = driver.find_element_by_class_name("rec-job-list")
            lst = element.find_elements_by_class_name("job-card-box")
            allOffer=[]
            # for e in element.find_elements_by_class_name("job-salary"):
            #     print(getStr(e.text));
            i = 1
            size = len(lst)
            print(size)
            hasApplyOffers = getHasApplyOffersByExcel()
            hasApplys = [f"{o.company}-{o.name}" for o in hasApplyOffers]
            for i in range(size):
                if i+1 < index:
                    continue
                a = lst[i]
                tags = []
                salary = getStr(a.find_element_by_xpath("div[1]/div/span").text)
                el = a.find_element_by_xpath("div[1]/div/a")
                name = el.text
                tagsEl = a.find_elements_by_xpath("div[1]/ul/li")
                company = a.find_element_by_class_name("boss-name").text
                for t in tagsEl: tags.append(t.text)
                of = BossOffer(name, tags, salary, company, el, tagsEl)
                #判断岗位是否已经申请,已申请则直接跳过
                #判断岗位是否符合要求
                if isComfortable(name, tags, salary, keywordLst, acquiretags) :
                    if f"{company}-{name}" in hasApplys:
                        continue
                    el.click()
                    time.sleep(2)
                    try:
                        address_el = driver.find_element_by_class_name("job-address-desc")
                        of.address = address_el.text
                        if not isContainer(addressTags, of.address):
                            continue
                    except NoSuchElementException:
                        print("address does not exist.")
                    # 立即沟通按钮
                    toChatElement = driver.find_element_by_class_name("op-btn-chat")
                    toChatElement.click()
                    time.sleep(2)
                    continueEl = driver.find_element_by_class_name("cancel-btn")
                    continueEl.click()
                    time.sleep(2)
                    allOffer.append(of)
                index = index + 1
            print(len(allOffer))
            saveExcel(allOffer)
            config.set('default', 'index', str(index))
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            lst[len(lst)-1].click()
            time.sleep(5)
            tmp += 1
    finally:
        # 释放锁
        lock.release()


def connectCurrentChrome(address='127.0.0.1:9222'):
    # 创建Chrome选项
    chrome_options = Options()
    # 设置debuggerAddress，这里的地址应替换为实际从步骤2中获得的调试URL
    chrome_options.add_experimental_option("debuggerAddress", address)
    # 创建一个新的WebDriver实例，指向已打开的浏览器会话
    return webdriver.Chrome(options=chrome_options)


if __name__ == '__main__':
    keywordLst = ["JAVA"]
    acquiretags = ["经验不限", "1年以内", "1-3年"]
    addressLst = ["广州"]
    sendResumeByKeyword(keywordLst, acquiretags, addressLst,1)
    # getHasApplyOffersByExcel();
