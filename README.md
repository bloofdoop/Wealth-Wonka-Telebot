# Wealth-Wonka-Telebot
I created a web parser Telegram bot for users to retrieve market news and daily prices based on a stock ticker symbol. This was part of a side project I had (wealthwonka.com) - a casual investing blog that I co-created alongside my good friends in 2020. It was meant to be a way to teach myself foundational financial modelling tools, and document that knowledge through articles and stock picks. Putting together the Telegram bot was also a way for me to train my Python skills and the first application I have successfully deployed live.

You can interact with the bot n Telegram through @wealthwonka_bot. Because the application is hosted on the free Heroku server, it will go into snooze every 30 minutes of inactivity. Therefore, the first time you type in the command "/start", it may take 10 seconds to respond. After which, the bot has been designed to be intuitive to use.

# Using python-telegram-bot
The main package I used was python-telegram-bot to run commands. I took inspiration from conversationbot.py (https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py) to create my ConversationHandlers and state functions.

Currently, the bot is able to fulfil three functions:
a) Get Price: get price statistics from MarketWatch when the user enters a ticker symbol
b) Get News: get the latest headlines from MarketWatch when the user enters a ticker symbol
c) Get Company: for users who are unsure what the ticker symbol for a company name (e.g. Apple) is, this function parses MarketWatch and returns the top 5 results corresponding to it (e.g. AAPL, ...)

I deployed my bot onto Heroku using a webhook so that users can interact with my bot without me having to run the code locally. A walkthrough that helped me with the process can be found here (https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2)

# Code
I uploaded the code into the file wealthwonkabot.py. The token address and Heroku app name have been redacted but feel free to clone the repository and add new functions of your own. You can go to @botfather on Telegram to get your own bot and simply substitute the address in my line TOKEN = '...' and the Heroku app name into webhook_url = '...'.

The requirements.txt - a text file of all the packages used and Procfile are also in the repository, these components are necessary for a successful build on Heroku. If you are importing any new packages into the .py file, you should add them to the requirements.txt before building on Heroku.

# Future changes
This bot is still in the works. I would like to add some new features to it that remember the user's choice and can provide daily updates (news, prices) at a certain time.
