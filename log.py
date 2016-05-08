#All the imports
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
    db.execute("SELECT * FROM logs LIMIT 1")
    if len(db.fetchall()) == 0:
        print "Database is empty."
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

def insert(postID, blog, content, tag, timestamp):
    db.execute("INSERT INTO logs (id, blog, content, tag, date) VALUES (%s, %s, %s, %s, %s)",
        (postID, blog, content, tag, timestamp))

def unique(post):
    postID = post["id"]
    db.execute("SELECT * FROM logs WHERE id=%s", (postID,))
    results = db.fetchall()
    return len(results) == 0

def getInfo(post, tag):
    postID = post["id"]  

    blog = post["blog_name"]                
    
    if post["type"] == "text":
        if len(post["trail"]) > 0:
            content = sanitize(post["trail"][0]["content"])
    elif post["type"] == "quote":
        if len(post["text"]) > 0:
            content = sanitize(post["text"])

    timestamp = post["timestamp"]  
    try:
        return (postID, blog, content, tag, timestamp)
    except UnboundLocalError:
        return None

#Loop through tags and log unique posts
try:
    print "Running..."
    for tag in tags:
        total = 0
        earliest = int(time.time()) #Bookmark for going back in time
        if mode == "run":
            db.execute("SELECT date FROM logs WHERE tag=%s ORDER BY date DESC LIMIT 1", (tag,))
            latest = db.fetchall()[0][0]

        quit = False
        while not quit:
            posts = client.tagged(tag, limit=20, before=earliest)
            try:
                earliest = min([ post["timestamp"] for post in posts ])
            except ValueError:
                quit = True
                break

            #if len(posts) == 0: #This means there are no posts left
            #    quit = True
            #    break

            for post in posts:
                if post != None and post["type"] in ["text", "quote"]:
                    info = getInfo(post, tag)
                    if info == None:
                        shouldAdd = False
                    else:
                        shouldAdd = True

                    if mode == "run" and post["timestamp"] < latest:
                        quit = True
                        break

                    if unique(post) and shouldAdd:
                        sys.stdout.flush()
                        total += 1
                        insert(*info)
                        sys.stdout.write('Found {0} posts with tag {1} timestamp {2}\r'.format(total, tag, earliest))
        print "\nDone " + tag + "\n"
    print "Finished."
except KeyboardInterrupt:
    print "\nExiting."

#Close connection
print "Closing connection to database."
db.close()
conn.close()
