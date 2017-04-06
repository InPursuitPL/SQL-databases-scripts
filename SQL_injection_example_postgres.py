#! python3
import psycopg2

def get_all_posts():
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute("SELECT time, content FROM posts ORDER BY time DESC")
    posts = ({'content': str(row[1]), 'time': str(row[0])}
             for row in c.fetchall())
    DB.close()
    return posts

def add_post_vulnerable(content):
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute("INSERT INTO posts (content) VALUES ('%s')" % content)
    DB.commit()
    BD.close()

def add_post_protected(content):
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute("INSERT INTO posts (content) VALUES ('%s')" % (content,))
    DB.commit()
    BD.close()

# Example to use for potential SQL injection.
add_post_vulnerable("'); delete from posts; --")
add_post_protected("'); delete from posts; --")





