from Tools.scripts.treesync import raw_input
import pymysql
import os

"""
mysql 表结构自动生成 java 实体类脚本
"""

conf_list = []


def adapter(text):
    """
    适配器
    :param text:
    :return:
    """
    if 'int' in text:
        return "Integer"
    if 'varchar' in text or 'char' in text or 'text' in text:
        return "String"
    if text == "bit" or "BOOLEAN".lower() in text:
        return "Boolean"
    if text == "datetime":
        return "Date"
    if "decimal" in text:
        return "BigDecimal"
    if "float" in text:
        return "Float"
    if "double" in text:
        return "Double"
    if "time" in text:
        return "Time"
    if "DATETIME".lower() in text:
        return "Timestamp"
    if "YEAR".lower() in text:
        return "Year"
    if "BIGINT".lower() in text:
        return "BigInteger"





if __name__ == '__main__':
    USERNAME = None
    PASSWORD = None
    HOSTNAME = None
    PORT = None
    DATABASE = None
    if os.path.exists("conf.init"):
        with open('conf.init', "r") as f:
            for line in f.readlines():
                conf_list.append(line)
            USERNAME = conf_list[0].replace("\n", "")
            PASSWORD = conf_list[1].replace("\n", "")
            HOSTNAME = conf_list[2].replace("\n", "")
            PORT = conf_list[3].replace("\n", "")
            DATABASE = conf_list[4].replace("\n", "")
    else:
        USERNAME = raw_input("username:").replace("\n", "")
        PASSWORD = raw_input("password:").replace("\n", "")
        HOSTNAME = raw_input("HOSTNAME:").replace("\n", "")
        PORT = raw_input("PORT:").replace("\n", "")
        DATABASE = raw_input("DATABASE:").replace("\n", "")
        with open('conf.init', "w") as f:
            f.write(USERNAME + "\n")
            f.write(PASSWORD + "\n")
            f.write(HOSTNAME + "\n")
            f.write(PORT + "\n")
            f.write(DATABASE + "\n")

    table = raw_input("表名:").replace("\n", "")
    name = raw_input("生成的实体类名:").replace("\n", "")

    sql = "SELECT column_name,column_type,column_key,column_comment,character_set_name from information_schema.columns WHERE table_schema = '%s' AND table_name = '%s';"

    conn = pymysql.connect(
        host=HOSTNAME,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        charset="utf8",
        port=int(PORT)
    )
    with open(name + ".java", "w", encoding="utf-8") as file:
        file.write("/**\n *auto  generate  by loafer \n */ \n")
        file.write("@Data\n")
        file.write("@Table(name =\"%s\" ) \n" % table)
        file.write("public class " + name + " { \n")

        with conn.cursor() as cursor:
            cursor.execute(sql % (DATABASE, table))
            for temp in cursor.fetchall():
                annotation = "   @Column(name = \"%s\")"
                file.write("   /**\n   * " + temp[3] + "\n   */\n")

                attribute = "   private %s  %s;"
                list = temp[0].split("_")
                attr = ""
                for i in list:
                    attr = attr + i[0].upper() + i[1:]
                attr = attr[0].lower() + attr[1:]
                print(attr)
                file.write(annotation % temp[0] + "\n")
                file.write(attribute % (adapter(temp[1]), attr) + "\n")
            file.write("}")
