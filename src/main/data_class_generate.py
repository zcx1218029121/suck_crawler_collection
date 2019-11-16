import pyodbc

"""
sql server 表结构自动生成 kotlin 实体类脚本
"""

table = "D_Product"
name = "Product"


def adapter(text):
    if text == "int" or text == "int identity":
        return "Int"
    if text == "nvarchar" or text == "ntext":
        return "String"
    if text == "bit":
        return "Boolean"
    if text == "datetime":
        return "Date"
    if text == "money" or text == "numeric":
        return "BigDecimal"


if __name__ == '__main__':

    conn = pyodbc.connect()

    with open(name + ".kt", "w", encoding="utf-8") as file:
        file.write("@Table(name =\"%s\" ) \n" % table)
        file.write("data class " + name + " (")
        with conn.cursor() as cursor:
            cursor.execute('sp_columns %s' % "D_Product")
            for temp in cursor.fetchall():
                annotation = " @Column(name = \"%s\")"
                sql = "var %s : %s?=null,"
                file.write(annotation % temp[3] + "\n")
                print(sql % (temp[3], adapter(temp[5])))
                file.write(sql % (temp[3], adapter(temp[5])) + "\n")
            file.write(")")
