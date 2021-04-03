import requests
from twilio.rest import Client
from _datetime import datetime
import os

my_api_key = os.environ.get("OWM_API_KEY")
my_latitude = 6.469700
my_longitude = 3.705700
accountsid = "AC7e1c93aa51c5bc98adef248b94dbc097"
auth_token = os.environ.get("AUTH_TOKEN")
phone_number = os.environ.get("PHONE_NUMBER")
current_hour = datetime.now().hour

response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={my_latitude}&lon={my_longitude}"
                        f"&exclude=[current,minutely,daily]&appid={my_api_key}")
response.raise_for_status()

it_will_rain = False
weather_code_list = []
for i in range(12):
    weather_code_list.append(response.json()["hourly"][i]["weather"][0]["id"])

rain_time = [f"{current_hour + i}AM" if current_hour + i < 12 else "12PM" if current_hour + i == 12
             else f"{current_hour + i - 12}PM" for i in range(len(weather_code_list))]

am_pm = ""
for i in range(12):
    if weather_code_list[i] < 700:
        am_pm += f" {rain_time[i]}"
        it_will_rain = True

if it_will_rain:
    client = Client(accountsid, auth_token)
    message = client.messages \
        .create(
            body=f"It's going to rain today at{am_pm}. Remember to take an ☔🌂",
            from_="+16672171230",
            to=f"{phone_number}"
        )
    print(message.status)
