import markovify
import nltk
import re
import numpy as np
import urllib
import oauth2 as oauth
from settings import conn, db, auth, post_tags, blogName


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        if words[0] != "":
            words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        else:
            words = list("",)
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


db.execute("SELECT body FROM fics ORDER BY date LIMIT 500")
posts = db.fetchall()
text = [post[0].strip() for post in posts]
text = " ".join(text)

text_model = POSifiedText(text, state_size=3)

output = ""
for i in range(abs(int(np.random.normal(9, 4, 1))) + 1):
    sentence = text_model.make_sentence()
    if sentence is not None:
        output += sentence.strip() + " "

title = text_model.make_short_sentence(70)


client = oauth.Client(
    oauth.Consumer(key=auth["consumer_key"], secret=auth["consumer_secret"]),
    oauth.Token(key=auth["oauth_token"], secret=auth["oauth_token_secret"])
)


resp, content = client.request(
    f"https://api.tumblr.com/v2/blog/{blogName}/post",
    method="POST",
    body=urllib.parse.urlencode({
        "title": title,
        "body": output,
        "tags": ",".join(post_tags),
        "format": "markdown"
    })
)
