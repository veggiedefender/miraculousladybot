# miraculousladybot
Logs tumblr fanfictions to a psql database and generates fanfictions using markov chains. You can see it in action [here](http://www.miraculousladybot.tumblr.com).

# Installation

Install [postgresql](http://www.postgresql.org/), add a user, and log in.

Create a database named `fanfictions`

`createdb fanfictions`

Run the install script to set up tables and columns 

`psql fanfictions -f create_tables.sql`

Install requirements with `pip`

`pip install -r requirements.txt`

# Setup

Edit `settings.py` with your information. You can get your Tumblr credentials [here](https://api.tumblr.com/console).

# Running it

## Running log.py
`python log.py`

## Running generate.py

`generate.py` will automatically generate and post a fanfiction. No setup is required if you have completed the previous steps. 

If you get an error like `TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'`, it's probably because you don't have enough data. Change `text_model = POSifiedText(text, state_size=3)` to `text_model = POSifiedText(text, state_size=2)`
