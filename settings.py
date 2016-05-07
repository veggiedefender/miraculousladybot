import pytumblr
import psycopg2

#Log in to tumblr
client = pytumblr.TumblrRestClient( #https://api.tumblr.com/console
    '<consumer_key>',
    '<consumer_secret>',
    '<oauth_token>',
    '<oauth_secret>',
)

#Connect to database
conn = psycopg2.connect("dbname=fanfictions user=postgres")
conn.autocommit = True
db = conn.cursor()

blogName = "miraculousladybot"

print "Loaded settings"