import datetime

import requests

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
VANTAGE_API = "5XZ72205U0P8REO8"
NEWS_API = "d1dd4b726bd740518b1c2321d8293cc9"

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

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={VANTAGE_API}&datatype=json"
response = requests.get(url)
data = response.json()

current_date = datetime.date.today()
one_day = datetime.timedelta(days=4)
yesterday = current_date - one_day
pre_yesterday = yesterday - datetime.timedelta(days=1)

yesterday_open = float(data['Time Series (Daily)'][str(yesterday)]["1. open"])
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

# print(
# f"Open yesterday {yesterday_open}\n Close pre-yesterday {pre_yesterday_close}\n Price change: {price_percentage_diff}%")
