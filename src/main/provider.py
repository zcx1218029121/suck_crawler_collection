from bs4 import BeautifulSoup
import requests
import time
import pymysql.cursors

import re
from Crawler.book_sql import book_sql


class provider:
    def __init__(self, start_url):
        self.start_url = start_url


def book(url, conn, sql):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "cookie": "Hm_lvt_fc36dd13d291f50d4944e1947213dcc0=1568684723,1568700465,1568708460,1568711088; Hm_lpvt_fc36dd13d291f50d4944e1947213dcc0=" + str(
            time.time())
    }
    r = requests.get(url, headers=header).text
    soup = BeautifulSoup(r, 'html.parser')
    # 书籍列表 详情链接列表
    book_des_list = soup.find_all("a", "read-more")
    for link in book_des_list:
        # 爬取书籍详情
        desBody = requests.get(link["href"], headers=header).text

        desSoup = BeautifulSoup(desBody, 'html.parser')
        if desSoup.find("h1", "kratos-entry-title text-center") is None:
            break
        book_name = desSoup.find("h1", "kratos-entry-title text-center").get_text()
        book_des = desSoup.find("div", "kratos-post-content").get_text()
        book_cover = desSoup.find("img")["src"]

        if desSoup.find("a", "downbtn") is not None:
            book_url = desSoup.find("a", "downbtn")["href"]
            print(book_url)
            try:
                true_downloader = requests.get(book_url, headers=header).text
            except Exception as e:
                break
            last_soup = BeautifulSoup(true_downloader, 'html.parser')
            if last_soup.find("div", "plus_l") is not None:
                book_code = last_soup.find("div", "plus_l").get_text()
                book_down = ''
                for down in last_soup.findAll("span", "downfile"):
                    if down.find("a") is not None:
                        book_down += down.find("a")["href"] + ","
                data = (book_name, book_cover, book_des, book_code, book_down)
            else:
                boodk_down_url = desSoup.find("a", "downbtn downcloud")["href"]
                code = book_des
                pattern = re.compile(r'提取码: ([a-z0-9]{4})')
                s = ""
                if len(re.findall(pattern, code)) > 0:
                    s = re.findall(pattern, code)[0]
                data = (book_name, book_cover, code, s, boodk_down_url)
            try:
                cur = conn.cursor()
                cur.execute(sql % data)
                conn.commit()
            except Exception as e:
                print(book_name)
                soup.find("a", "")

    if soup.find("a", "next") is None:
        return
    # else:
    # return book(soup.find("a", "next")["href"], conn, sql)


if __name__ == '__main__':
    start_time = time.time()
    conn = book_sql().get_con()
    sql = "insert into book_copy1 (book_name,book_cover,book_des,book_code,book_link) values (\'%s\',  \'%s\' ,\'%s\',  " \
          "\'%s\',\'%s\') "

    book("https://www.d4j.cn/page/129", conn, sql)

    conn.close()
    end_time = time.time()
    print(end_time - start_time)
