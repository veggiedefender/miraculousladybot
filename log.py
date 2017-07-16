import requests
import time
import psycopg2
from datetime import datetime
from html2text import html2text
from settings import conn, db, auth, log_tags

url = f"https://api.tumblr.com/v2/tagged?api_key={auth['consumer_key']}&tag="


def get(url):
    while True:
        try:
            r = requests.get(url).json()
            assert r is not None
            assert r["meta"]["msg"] == "OK"
        except Exception:
            time.sleep(1)
            continue
        break
    return r


for tag in log_tags:
    total = 0
    earliest = int(datetime.now().timestamp())
    quit = False
    while not quit:
        posts = get(f"{url}{tag}&before={earliest}")["response"]
        if len(posts) == 0:
            quit = True
            break
        earliest = min([post["timestamp"] for post in posts])
        posts = [post for post in posts if post["type"] == "text"]
        for post in posts:
            try:
                id = post["id"]
                body = html2text(post["body"])
                timestamp = post["timestamp"]
                db.execute("""INSERT INTO fics (id, body, date)
                           VALUES (%s, %s, %s)""", (id, body, timestamp))
                conn.commit()
                total += 1
                print(f"{tag}: {total}\r", end="")
            except Exception:
                conn.rollback()
    print()
