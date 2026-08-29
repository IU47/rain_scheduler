import os
import requests
from twilio.rest import Client
import smtplib


api_key = os.environ["OWM_API_KEY"]

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

MY_EMAIL = os.environ["MY_EMAIL"]
MY_PASSWORD = os.environ["MY_PASSWORD"]

MY_LAT = float(os.environ["MY_LAT"])
MY_LONG = float(os.environ["MY_LONG"])

MY_PHONE = os.environ["MY_PHONE"]
TWILIO_PHONE = os.environ["TWILIO_PHONE"]


client = Client(account_sid, auth_token)


params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": api_key,
    "cnt": 4
}


response = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params=params
)

response.raise_for_status()

weather_data = response.json()


# Check if it will rain
will_rain = False

for hour_data in weather_data["list"]:

    condition = hour_data["weather"][0]["id"]

    if condition < 700:
        will_rain = True


if will_rain:

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:

        connection.starttls()

        connection.login(
            MY_EMAIL,
            MY_PASSWORD
        )

        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=(
                "Subject:Brace for Impact!\n\n"
                "Don't forget your umbrella if you're going out. "
                "It's about to rain!"
            )
        )

    message = client.messages.create(
        body="sms_event_notifications",
        from_=TWILIO_PHONE,
        to=MY_PHONE
    )

    print(message.status)
