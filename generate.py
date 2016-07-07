import markovify
import nltk
import re
import random
from settings import client, conn, db, blogName

#Tags
tags = ["miraculous ladybug", 
    "fanfiction", 
    "miraculous", 
    "ladybug"]

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        if words[0] != "":
            words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        else:
            words = list('',)
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

db.execute("SELECT content FROM logs ORDER BY date LIMIT 500")
text = [ post[0] for post in db.fetchall() ]
text = ''.join(text)

text_model = POSifiedText(text, state_size=3)

#Get a random length skewed toward shorter ones
def get_i():
    f = random.randint(1, 20)
    if f < 15: #Short post
        i = random.randint(1, 5)
    else:      #Longer post
        i = random.randint(5, 20)
    return i

output = ""
for i in range(get_i()):
    output += text_model.make_sentence() + " "
 
title = text_model.make_short_sentence(70)
print title, "-", output
client.create_text(blogName, state="published", title=title, body=output, tags=tags, format="markdown")
