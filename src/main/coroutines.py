import queue
import time
import requests
import threading
from bs4 import BeautifulSoup
import re

flag = True
g_num = 5
mutex = threading.Lock()

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "cookie": "Hm_lvt_fc36dd13d291f50d4944e1947213dcc0=1568684723,1568700465,1568708460,1568711088; Hm_lpvt_fc36dd13d291f50d4944e1947213dcc0=" + str(
        time.time())
}
# 数据列表urL 爬虫
item_queue = queue.Queue()
# 数据列表url 爬虫
pager_queue = queue.Queue()


def spider_pager(url):
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    # 书籍列表 详情链接列表
    book_des_list = soup.find_all("a", "read-more")
    for temp in book_des_list:
        item_queue.put(temp["href"])
    if soup.find("a", "next") is None:
        global flag
        flag = False
        return
    else:
        return spider_pager(soup.find("a", "next")["href"])


def spider_item():
    # 生产者线程 闲置 且 消息队列为空的情况下 结束消费
    while flag or not item_queue.empty():
        des_body = requests.get(item_queue.get(), headers=header).text
        soup = BeautifulSoup(des_body, 'html.parser')
        code = soup.find("div", "kratos-post-content").get_text()
        print("正在爬取 " + soup.find("h1", "kratos-entry-title text-center").get_text())
        if soup.find("a", "downbtn downcloud") is not None:
            pattern = re.compile(r'提取码: ([a-z0-9]{4})')
            if len(re.findall(pattern, code)) > 0:
                out = re.findall(pattern, code)[0]
                output_link_and_code(soup.find("a", "downbtn downcloud")["href"].replace(",", " ") + out + "\n")
        elif soup.find("a", "downbtn") is not None:
            book_url = soup.find("a", "downbtn")["href"]
            pager_queue.put(book_url)
    # 为 活跃线程数 加锁
    mutex.acquire()
    global g_num
    g_num = g_num - 1
    mutex.release()


def spider_book():
    while g_num != 0 or not pager_queue.empty():
        if not pager_queue.empty():
            des_body = requests.get(pager_queue.get(), headers=header).text
            soup = BeautifulSoup(des_body, 'html.parser')
            if soup.find("div", "plus_l") is not None:
                book_code = soup.find("div", "plus_l").get_text()
                book_down = ''
                for down in soup.findAll("span", "downfile"):
                    if down.find("a") is not None:
                        book_down += down.find("a")["href"] + ","
                pattern = re.compile(r'百度网盘提取码 ：([a-z0-9]{4})')
                if len(re.findall(pattern, book_code)) > 0:
                    dd = re.findall(pattern, book_code)[0]
                    output_link_and_code(book_down.replace(",", " ") + dd + "\n")
    print("===========爬取结束 ================= ")


def output_link_and_code(txt):
    with open("百度网盘链接.txt", "a") as f:
        f.write(txt)


print("开始爬取.....")
print("爬取结果将生成为百度网盘链接.txt")
t = threading.Thread(target=spider_pager, args=("https://www.d4j.cn/page/120",))
t.start()
# 启动消费者 & 生产者 线程 5 条 把爬取到的内容 放到 队列中
for i in range(0, 5):
    s = threading.Thread(target=spider_item, args=())
    s.start()

for j in range(0, 5):
    m_threading = threading.Thread(target=spider_book, args=())
    m_threading.start()
