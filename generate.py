#All the imports
import markovify
import pytumblr
import psycopg2
import random

from settings import client, conn, db, blogName

#Tags
tags = ["miraculous ladybug", 
    "fanfiction", 
    "miraculous", 
    "ladybug"]

#Build the model.
db.execute("SELECT content FROM logs")
text = [ post[0] for post in db.fetchall()]
text = ''.join(text)

text_model = markovify.Text(text)
print "Generated model."

#Get a random length skewed toward shorter ones
def get_i():
    f = random.randint(1, 20)
    if f < 15: #Short post
        i = random.randint(1, 5)
    else:      #Longer post
        i = random.randint(5, 20)
    return i

#Generate the body
output = ""
for i in range(get_i()):
    output += text_model.make_sentence() + " "

#Generate the title    
title = text_model.make_short_sentence(70)
print title, "-", output
client.create_text(blogName, state="published", title=title, body=output, tags=tags, format="markdown")