import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API = "e3042fb842cb4bd2a0fb304e6e666ad9"
STOCK_API = "A1NX3I4XO10B7ZUN"

STOCK_PARAM = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_API
}

NEWS_PARAM = {
    "q": COMPANY_NAME,
    "apikey": NEWS_API
}

TWILLO_SID = "ACd1dc43b2a16f4364690bb06b6abfd853"
AUTH_TOKEN = "8ceda03ee1b3d87c701a8507f5b8654b"

# STEP 1: Use https://www.alphavantage.co/documentation/#daily

response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAM)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
# e.g. [new_value for (key, value) in dictionary.items()]

data_list = [value for (key, value) in stock_data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])

# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
# Hint: https://www.w3schools.com/python/ref_func_abs.asp

diffrence = (yesterday_closing_price - day_before_yesterday_closing_price)
up_down = None
if diffrence > 1:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
percentage_diffrence = round((diffrence / yesterday_closing_price) * 100)

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

if abs(percentage_diffrence) > 0:
    response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAM)
    response.raise_for_status()
    # Use Python slice operator to create a list that contains the first 3 articles.
    # Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    articles = response.json()["articles"]
    three_articles = articles[:3]
    # Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article_list = [
        f"{STOCK}: {up_down}{abs(percentage_diffrence)}%\nHeadline: {article['title']}."
        f"\nBrief: {article['description']}" for article in three_articles
    ]
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    client = Client(TWILLO_SID, AUTH_TOKEN)
    # Send each article as a separate message via Twilio.

    for article in formatted_article_list:
        message = client.messages.create(
            body=article,
            from_="+19705077060",
            to="+2347068827272"
        )

        print(message.status)
        
        
