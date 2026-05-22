import requests
import requests_cache
import os

requests_cache.install_cache('company_cache')

STOCK = "EPAM"
COMPANY_NAME = "Epam Systems Inc"
STOCK_API_KEY = "OM6T1HIRVQE8RTI9"
NEWS_API_KEY = "64b87320358944159b4ae9b1f16b6d91"
WEATHER_API_KEY = "253682c0bd759acfb4255d4aa08c3dd7"

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chatID = os.environ.get("BOT_CHAT_ID")
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def get_weather_data():
    params = {
        "lat": "49.9935",
        "lon": "36.230383",
        "appid": WEATHER_API_KEY,
        "cnt": 4
    }

    response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast", params=params)
    response.raise_for_status()
    weather_data = response.json()

    return weather_data

def get_company_info(company_name: str):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY
    }

    url = "https://www.alphavantage.co/query"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        company_data = response.json()["Time Series (Daily)"]
        source: str = 'CACHE' if getattr(response, "from_cache", False) else 'API'

        data_list = [value for (key, value) in company_data.items()]

        return {
            "Source": source,
            "name": company_name,
            "Company data": data_list,
        }
    except Exception as e:
        return {f"Error from {url}": f"{e}"}

def get_news(company_name: str):
    params = {
        "qInTitle": company_name,
        "apiKey": NEWS_API_KEY
    }
    url = "https://newsapi.org/v2/everything"

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        news_data = response.json()
        source: str = 'CACHE' if getattr(response, "from_cache", False) else 'API'

        return {
            "Source": source,
            "name": company_name,
            "News data": news_data["articles"][:3],
        }
    except Exception as e:
        return {f"Error from {url}": f"{e}"}

def main_weather():
    data = get_weather_data()

    weather_list = [item["weather"][0]["id"] for item in data["list"]]

    is_raining = False
    for item in weather_list:
        if int(item) < 800:
            is_raining = True

    if is_raining:
        telegram_bot_sendtext("Raining")

def main_company():
    company_info = get_company_info(COMPANY_NAME)
    yesterday_price = float(company_info["Company data"][0]["4. close"])
    day_before_yesterday_price = float(company_info["Company data"][1]["4. close"])

    dif_percent = round((abs(yesterday_price - day_before_yesterday_price) / yesterday_price) * 100)

    if abs(dif_percent) > 1:
        news = get_news(COMPANY_NAME)
        last_news = news["News data"]

        list_articles = [f"Headline: {article['title']}\nBrief: {article['description']}" for article in last_news]

        mark = "🔺" if (yesterday_price - day_before_yesterday_price) > 0 else "🔻"
        message = f"""
        {STOCK}: {mark}{dif_percent}%
        {'\n'.join(list_articles)}
        """

        telegram_bot_sendtext(message)

main_weather()
main_company()
