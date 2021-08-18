

import logging
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)
TOKEN = '...'

CHOOSING, PRICE, NEWS, SYMBOL = range(4)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    reply_keyboard = [['Get Price', 'Get News', 'Get Symbol']]
    
    update.message.reply_text(
        'Hi! I am the Wealth Wonka. You can get the latest information about a stock.'
        'Send /cancel to stop talking to me or /start to return to this menu.\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True
            ),
        )
    return CHOOSING

# See which function the user chose from thi reply keyboard
def check_user_input(update: Update, context: CallbackContext)->int:
    user_data = update.message.text
    if user_data == 'Get Price':
        update.message.reply_text("Reply with the ticker symbol for a stock to get its price")
        return PRICE
    if user_data == 'Get News':
        update.message.reply_text("Reply with the ticker symbol for a stock to get latest headlines")
        return NEWS
    if user_data == 'Get Symbol':
        update.message.reply_text("Reply with a company name to get its ticker symbol")
        return SYMBOL

# State functions corresponding to they reply keyboard choice the user makes
def get_tickerprice(update: Update, context:CallbackContext):
    ticker_symbol = update.message.text
    print_price(update, context, ticker_symbol)
    prompt = "Send another ticker to get its price, or use /start to return to the main menu and " \
        "/cancel to exit the conversation"
    update.message.reply_text(prompt)
    return 
    
def get_tickernews(update: Update, context:CallbackContext):
    ticker_symbol = update.message.text
    print_headlines(update, context, ticker_symbol)
    prompt = "Send another ticker to get latest headlines, or use /start to return to the main menu and " \
        "/cancel to exit the conversation"
    update.message.reply_text(prompt)
    return 

def get_tickersymbol(update: Update, context:CallbackContext):
    company = update.message.text
    print_tickers(update, context, company)
    prompt = "Send another company name to get its ticker symbol, or use /start to return to the main menu and " \
        "/cancel to exit the conversation"
    update.message.reply_text(prompt)
    return 
        

# Web scraping functions

def print_price(update: Update, context: CallbackContext, ticker_symbol):
    ticker_symbol = update.message.text
    price_result = price_search(ticker_symbol)
    if price_result != "":
        update.message.reply_text(price_result)
    else:
        update.message.reply_text('Sorry, no results were found')

def price_search(ticker_symbol):
    url = "https://www.marketwatch.com/investing/stock/" + ticker_symbol
    req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
    response = urlopen(req)
    soup = BeautifulSoup(response, "lxml")
    
    
    # Create a list for labels and corresponding values
    labels = []
    values = []
    
    ip = soup.find('h2', attrs={'class':'intraday__price'}).get_text()
    ip = ip.replace("\n","").rstrip()
    
    labels.append("Intraday Price")
    values.append(ip)
    
    soup = soup.findAll('li',attrs={'class': 'kv__item'})
    for x in soup:
        label = x.find('small').contents[0]
        value = x.find('span').contents[0]
        labels.append(label)
        values.append(value)
    
    label_numbers= [1,2,3,7,8,9,10,12,13,14,15]
    text = ""
    for label_number in label_numbers:
        text += labels[label_number] + ": " + values[label_number] + "\n"
    return text


def print_headlines(update: Update, context: CallbackContext, ticker_symbol):
    headlines_list = headlines_search(ticker_symbol)
    result = ''
    if headlines_list == []:
        update.message.reply_text('Sorry, no results were found.')
    else:
        update.message.reply_text("These are the top headlines for your stock today.")
        for hL in headlines_list:
            result += " <a href='" + hL['link'] + "'>" + hL['text'] + "</a>\n\n"
            
    
        update.message.reply_html(result, disable_web_page_preview=True)

def headlines_search(ticker_symbol):
    # Search tickers using MArketWatch
    url = "https://www.marketwatch.com/investing/stock/" + ticker_symbol
    
    # create an empty list to store ticker results
    headlines_list = []
    
    # get search results using the news_url
    req = Request(url=url, headers={'user-agent': 'my-app/0.0.1'})
    response = urlopen(req)
    
    # get response using BeautifulSoup and store in 
    soup = BeautifulSoup(response, "lxml")
    soup = soup.findAll('h3',attrs={'class': 'article__headline'})
    
    # search only the top 5 most recent headlines
    for x in soup[:5]:
        if x.find('a') is not None:
            headlines = {}
            text = x.get_text().strip()
            link = x.a.get('href')
            headlines["text"] = text
            headlines["link"] = link
            headlines_list.append(headlines)
    
    return headlines_list

def print_tickers(update: Update, context: CallbackContext, company):
    # Format a search consisting of multiple words
    search_string = company.replace(' ', '-')
    update.message.reply_text(company_search(search_string))
    
def company_search(search_string):
    text = ''
    company_url = "https://finance.yahoo.com/lookup?s=" + search_string

    req = Request(url=company_url, headers={'user-agent': 'my-app/0.0.1'})
    response = urlopen(req)

    # get response via BeautifulSoup
    soup = BeautifulSoup(response, "lxml")

    x = soup.findAll(attrs={'class': 'lookup-table W(100%) Pos(r) BdB Bdc($seperatorColor) smartphone_Mx(20px)'})
    result = []
    for tr in x:
        result.extend(tr.find_all(attrs={'class': 'data-col0 Ta(start) Pstart(6px) Pend(15px)'}))

    # This returns the top 5 rows
    result = result[:5]

    # This extracts the symbol and company name from the bs4 element and puts them into a list
    symbols = []
    company_names = []
    if len(result) > 0:
        for element in result:
            element = element.contents[0]
            company_name = element.get('title')
            company_names.append(company_name)
            symbol = element.get_text()
            symbols.append(symbol)
    
        # this prints out the top 5 rows in the form of symbol, company name
        for i in range(len(result)):
            text += ("Ticker " + symbols[i] + " for company " + company_names[i]) + '\n\n'
    else:
        text = "Sorry, no results were found."
    return text

def cancel(update: Update, context: CallbackContext):

    """Cancels and ends the conversation"""
    update.message.reply_text(
        'Hope you got what you needed!', reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END
        
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states PRICE, NEWS, SYMBOL
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
                CHOOSING: [MessageHandler(Filters.regex('^(Get Price|Get News|Get Symbol)$'), check_user_input),],
                PRICE: [MessageHandler(Filters.text & ~Filters.command, get_tickerprice),],
                NEWS: [MessageHandler(Filters.text & ~Filters.command, get_tickernews),],
                SYMBOL: [MessageHandler(Filters.text & ~Filters.command, get_tickersymbol),],
                },
        # See if we can lead the state to prompt a new one or press /cancel to end the conversation
        fallbacks=[CommandHandler('cancel', cancel), CommandHandler('start', start)],
    )
    
    dp.add_handler(conv_handler)
    
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen='0.0.0.0',port=int(PORT),url_path=TOKEN,
                          webhook_url='...'+TOKEN)


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
