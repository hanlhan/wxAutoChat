from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

import MySQLdb

mysqldb = MySQLdb.connect("localhost", "root", "1234", "wx", charset='utf8' )
mysqlcursor = mysqldb.cursor()


es = Elasticsearch()

# with open("AI.csv", 'r', encoding='utf-8') as line_list:
    # my_mapping = {"mappings": {"context": {
    #         "properties": {"context": {"type": "text"}, "split_word": {"type": "text"}, "context_id": {"type": "text"}}}}}
    # # 创建Index和mapping
    
    # es.indices.delete(index="article", ignore=[400, 404])
    # create_index = es.indices.create(
    #     index="article", body=my_mapping)  # {u'acknowledged': True}

    # if create_index["acknowledged"] != True:
    #     print("Index data bug...")

sql = "select * from article"
mysqlcursor.execute(sql)
results = mysqlcursor.fetchall()

es.indices.delete(index='article', ignore=[400, 404])

    # 创建ACTIONS
ACTIONS = []
for row in results:
    action = {
        "_index": 'artice',
        "_type": 'context',
        "_source": {
            "title": row[0],
            "content_url": row[1],
            "datetime": row[2]
        },
    }
    ACTIONS.append(action)
    # 批量处理
print(len(ACTIONS))

print(ACTIONS[0])
success = bulk(es, ACTIONS, index="artice")

print("finish")