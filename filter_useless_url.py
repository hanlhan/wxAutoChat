#coding: UTF-8
import requests

import urllib
import MySQLdb


mysqldb = MySQLdb.connect("localhost", "root", "1234", "wx", charset='utf8' )
mysqlcursor = mysqldb.cursor()

sql = "select content_url from article"

mysqlcursor.execute(sql)
results = mysqlcursor.fetchall()
string = "该内容已被发布者删除"

bytes(string, encoding = "utf8")

i = 0
for res in results:
    response = requests.request("GET", res[0])


    if string in response.text:
        sql2 = "delete from article where content_url='"+res[0]+"'"
        try:
            print(i)
            # 执行SQL语句
            mysqlcursor.execute(sql2)
            # 提交修改
            mysqldb.commit()
            i+=1
        except Exception as e:
            print(str(e))
            # 发生错误时回滚
            mysqldb.rollback()
        

print(i)
print("finished!")
mysqldb.close()


