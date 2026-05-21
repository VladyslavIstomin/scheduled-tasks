import requests
import os

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("BOT_TOKEN")
    bot_chatID = os.environ.get("BOT_CHAT_ID")
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

api_key = "253682c0bd759acfb4255d4aa08c3dd7"
params = {
    "lat": "49.9935",
    "lon": "36.230383",
    "appid": api_key,
    "cnt": 4
}

response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast", params=params)
response.raise_for_status()
data = response.json()

weather_list = [item["weather"][0]["id"] for item in data["list"]]

is_raining = False
for item in weather_list:
    if int(item) < 800:
        is_raining = True

if is_raining:
    telegram_bot_sendtext("Raining")
