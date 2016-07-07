# miraculousladybot
Logs tumblr fanfictions to a psql database and generates fanfictions using markov chains. You can see it in action [here](http://www.miraculousladybot.tumblr.com).

# Installation

Install [postgresql](http://www.postgresql.org/), add a user, and log in.

Create a database named `fanfictions`

`createdb fanfictions`

Run the install script to set up tables and columns 

`psql fanfictions -f create_tables.sql -U your_username -h localhost -W`

Install requirements with `pip`

`pip install -r requirements.txt`

# Setup

Edit `settings.py` with your information. You can get your Tumblr credentials [here](https://api.tumblr.com/console). 

Change `blogName` to the name of the blog you want to post to. 

Edit connection info if your database is set up differently.

Edit the tags in both `log.py` and `generate.py`. The tags in `log.py` are the tags that are searched, while the tags in `generate.py` are the tags included in each post.

# Running it

## Running log.py
`log.py` runs in two modes. 

The first mode, `sync` will find *every* unique fanfiction with the associated tags. This will run in two cases:

1. When the `fanfictions` database is empty
2. When you add **anything** to the command line arguments. For example, `python log.py sync` will trigger it as well as `python log.py sandwiches`.

I recommend running `log.py` in sync mode once every 24 hours to catch anything the logger may have missed.

The second mode, `run` is the default. It will "update" the database with any new posts. It's much faster than sync mode but may miss a few posts.

## Running generate.py

`generate.py` will automatically generate and post a fanfiction. No setup is required if you have completed the previous steps. 

If you get an error like `TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'`, it's probably because you don't have enough data. Change `text_model = POSifiedText(text, state_size=3)` to `text_model = POSifiedText(text, state_size=2)`
