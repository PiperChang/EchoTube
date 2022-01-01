import pandas as pd
from sqlalchemy import create_engine
import pymysql.cursors


data = pd.read_csv("./_csv_youtube_trending_data.csv")

publishedAt = data[['publishedAt']]
data = data[['index','video_id','title','publishedAt','categoryId','tags']]


connection = pymysql.connect(host='localhost',
                            user='root',
                            password='0000',
                            db='mydb',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

try:
    cursor = connection.cursor()
    
    for index, row in data.iterrows():
        sql = "insert into videos(id,video_id_name,title,published_at,category_id,tags) values(%s,%s, %s, %s,%s,%s)"
        categoryId = int(row['categoryId'])
        cursor.execute(sql,(row['index'],row['video_id'],row['title'],row['publishedAt'],categoryId,row['tags']))
        connection.commit()


    
    #print(cursor.fetchall())
    
    #rows = cursor.fetchall()
    #for i in rows :
     #print(i)
finally:
    cursor.close()
    connection.close()