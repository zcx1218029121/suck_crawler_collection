import pymysql.cursors
import re

if __name__ == '__main__':
    conn = pymysql.connect(host='120.79.55.82',
                           user='root',
                           port=3307,
                           password='root',
                           db='book',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    with open("auto.txt", "w+") as f:

        with conn.cursor() as cursor:
            cursor.execute("select book_link ,book_code from book;")
            lists = cursor.fetchall()

            for temp in lists:
                pattern = re.compile(r'百度网盘提取码 ：([a-z0-9]{4})')
                if len(re.findall(pattern, temp['book_code'])) > 0:
                    s = re.findall(pattern, temp['book_code'])[0]
                    f.write(temp['book_link'].replace(",", " ") + s + "\n")
