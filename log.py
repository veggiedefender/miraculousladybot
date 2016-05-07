#All the imports
import psycopg2
import pytumblr
import time
from bs4 import BeautifulSoup
import sys

from settings import client, conn, db, blogName

#Tags
tags = ["miraculous ladybug fanfiction", 
    "miraculous ladybug fanfic", 
    "ml fanfiction", 
    "ml fanfic", 
    "ladybug fanfiction", 
    "ladybug fanfic", 
    "miraculous fanfiction", 
    "miraculous fanfic", 
    "adrinette", 
    "ladynoir", 
    "ladrien",
    "marichat"]

#Set the mode. Two options: sync and run
if len(sys.argv) > 1:
    mode = "sync"
else:
    mode = "run"
    db.execute("SELECT date FROM logs ORDER BY date DESC LIMIT 1")
    try:
        latest = db.fetchall()[0][0]
    except IndexError:
        mode = "sync"
print "Running in mode %s" % mode.upper()

#Some helper functions
def sanitize(value):
    #Strip HTML
    soup = BeautifulSoup(value, "html.parser")
    for tag in soup.findAll(True):
        tag.hidden = True
    content = soup.renderContents()

    #Remove duplicate whitespaces/newlines
    content = content.replace("\n", " ")
    return ' '.join(content.split()) + "\n"

def insert(postID, blog, content, timestamp):
    db.execute("INSERT INTO logs (id, blog, content, date) VALUES (%s, %s, %s, %s)",
        (postID, blog, content, timestamp))

def unique(postID):
    db.execute("SELECT * FROM logs WHERE id=%s", (postID,))
    results = db.fetchall()
    return len(results) == 0

#Loop through tags and log unique posts
try:
    print "Running..."
    for tag in tags:
        earliest = int(time.time()) #Bookmark for going back in time

        quit = False
        while not quit:
            posts = client.tagged(tag, limit=20, before=earliest)

            for post in posts:
                if post != None: #Sometimes tumblr API returns None
                    blog = post["blog_name"]

                    if blog != blogName and post["type"] in ["quote", "text"]:
                        timestamp = post["timestamp"]

                        if mode == "run" and timestamp < latest:
                            quit = True
                            break

                        if timestamp < earliest:
                            earliest = timestamp

                        postID = post["id"]                    
                        
                        if post["type"] == "quote":
                            if len(post["text"]) > 0:
                                content = sanitize(post["text"])

                        elif post["type"] == "text":
                            if len(post["trail"]) > 0:
                                content = sanitize(post["trail"][0]["content"])

                        if unique(postID):
                            insert(postID, blog, content, timestamp)
            if len(posts) == 0: #This means there are no posts left
                quit = True
    print "Finished."
except KeyboardInterrupt:
    print "\nExiting."

#Close connection
print "Closing connection to database."
db.close()
conn.close()