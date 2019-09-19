import pymysql.cursors


class book_sql:

    def __init__(self, host="120.79.55.82", port=3307, user_name="root", pass_words="root", db='book'):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.user_name = pass_words
        self.conn = pymysql.connect(host=host,
                                    user=user_name,
                                    port=port,
                                    password=pass_words,
                                    db=db,
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)

    def get_con(self):
        return self.conn
