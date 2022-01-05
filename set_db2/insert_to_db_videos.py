import pandas as pd
import pymysql.cursors


data = pd.read_csv("./_csv_youtube_trending_data.csv")

publishedAt = data[['publishedAt']]
data = data[['index', 'video_Address', 'title', 'publishedAt', 'channelTitle'
             'categoryId', 'tags', 'likes', 'view_count', 'thumbnail']]


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='0000',
                             db='mydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    cursor = connection.cursor()
    for index, row in data.iterrows():
        sql = "insert into videos(id,video_address,title,published_at,category_number,tags,\
                likes, views, thumbnail, channel)\
               values(%s,%s, %s, %s,%s,%s,%s,%s,%s,%s)"
        category_number = int(row['categoryId'])
        cursor.execute(sql, (row['index'], row['video_Address'], row['title'],
                             row['publishedAt'], category_number, row['tags'],
                             row['likes'], row['view_count'], row['thumbnail'],
                             row['channel']))
        connection.commit()
        
finally:
    cursor.close()
    connection.close()
