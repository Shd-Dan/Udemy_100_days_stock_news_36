import datetime
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
VANTAGE_API = "5XZ72205U0P8REO8"
NEWS_API = "d1dd4b726bd740518b1c2321d8293cc9"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
TWILIO_SID = "#################################"
TWILIO_AUTH = "################################"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""TSLA: 🔺2% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey have 
gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 
or "TSLA: 🔻5% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey 
have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus 
market crash."""

""" -------------------------------------------- My Solution -------------------------------------------- """
"""
url = (f"https://www.alphavantage.co/query?"
       f"function=TIME_SERIES_DAILY&"
       f"symbol={STOCK}&"
       f"apikey={VANTAGE_API}&"
       f"datatype=json")
response = requests.get(url)
data = response.json()


def get_prices(day: int):
    current_date = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = current_date - one_day
    pre_yesterday = yesterday - datetime.timedelta(days=day)

    yesterday_open = float(data['Time Series (Daily)'][str(yesterday)]["4. close"])
    pre_yesterday_close = float(data['Time Series (Daily)'][str(pre_yesterday)]["4. close"])
    price_percentage_diff = (((yesterday_open / pre_yesterday_close) * 100) - 100).__round__(2)

    if price_percentage_diff > 1:

        news_url = (f"https://newsapi.org/v2/everything?"
                    f"q=tesla&"
                    f"from={str(yesterday)}&"

                    f"sortBy=publishedAt&"
                    f"language = en&"
                    f"apiKey={NEWS_API}"
                    )
        news_response = requests.get(news_url)

        first_articles = news_response.json()["articles"][:3]
        for article in first_articles:
            print(f"Title: {article['title']}\n Description: {article['description']}")

    elif price_percentage_diff < 1:
        print("Price change is inevitable")


try:
    get_prices(1)
except KeyError:
    get_prices(3)
"""

""" -------------------------------------------- Angela's Solution -------------------------------------------- """
## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": VANTAGE_API,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']


# TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_data_closing_price = day_before_yesterday_data["4. close"]


# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
#  Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = abs(float(yesterday_closing_price) - float(day_before_yesterday_data_closing_price))


# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price
#  the day before yesterday.
diff_percent = (difference / float(yesterday_closing_price)) * 100


# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
# pass to TODO6

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
if diff_percent > 0.1:
    news_params = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = articles[:3]


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

formatted_article = [f"Headlines: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
# TODO 9. - Send each article as a separate message via Twilio.
client = Client(TWILIO_SID, TWILIO_AUTH)
for article in formatted_article:
    message = client.messages.create(
        from_='+17624659325',
        body=article,
        to='+77072690628'
    )