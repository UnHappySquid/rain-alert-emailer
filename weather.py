import requests
import sys
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
import time


def setup():
    """
    Sets up global variables
    """
    global WEATHER_API_KEY, EMAIL_API_KEY, SENDER, ALPHA3_TO_ISO, TARGET_EMAIL, TODAY

    TODAY = time.localtime()

    # This program uses https://openweathermap.org/ for weather requests,
    # and sendgrip for email sending, need to set your own api keys and other important values
    # in a file called api-keys.json, refer to ./README.md for more details
    with open("api-keys.json", "r") as creds:
        json_file = creds.read()
        api_obj = json.loads(json_file)
        WEATHER_API_KEY = api_obj["OpenWeatherKey"]
        EMAIL_API_KEY = api_obj["SendGridKey"]
        SENDER = api_obj["SendGridSender"]
        TARGET_EMAIL = api_obj["TargetEmail"]

    # gets Country to ISO mapping
    with open("data/iso-3166-code.json") as iso:
        json_file_content = iso.read()
        raw_json = json.loads(json_file_content)
        ALPHA3_TO_ISO = {}
        for att in raw_json:
            ALPHA3_TO_ISO[att["alpha-3"]] = att["name"]


def prompt():
    """
    Prompts user for information
    :return: a tuple of the inputted city and country, in that order.
    """
    print("WEATHER FORECASTER, FOLLOW THE FOLLOWING INSTRUCTIONS AND GET THE WEATHER")
    print("*" * 100)
    print("Please input the following information with the first letter of every word upperCased,"
          "and only using ascii characters")
    city = input("Input City : ")
    country = input("Input country's alpha 3 : ")
    return (city, country)


def get_weather_information(city, country):
    """
    Fetches the city, country's weather information.
    :param city: city whose weather we want to fetch
    :param country: the country of that city in alpha-3 form
    :return: https://openweathermap.org/ response to request.
    """
    country_iso = ALPHA3_TO_ISO[country]
    try:
        response = requests \
            .get(f"https://api.openweathermap.org/data/2.5/weather?"
                 f"q={city},{country_iso}&appid={WEATHER_API_KEY}&units=metric", timeout=5)
    except requests.exceptions.Timeout:
        exit(f"Request Time out.")

    if not response.ok:
        exit(f"Request failed, Response : \n{response}\n{response.content}")

    api_response = response.json()

    return api_response


def bad_weather(response):
    """
    Checks if the weather is misty, if it will snow, rain or if there will be a storm
    :param response: https://openweathermap.org/ response to weather request.
    :return: true if to expect bad weather, false otherwise.
    """
    weather_id_code = int(response["weather"][0]["id"] / 100)
    return weather_id_code == 2 or weather_id_code == 5 or weather_id_code == 6 or weather_id_code == 7


def send_alert_email(description, temp, humidity):
    """
    Sends an email with the appropriate description, temperature and humidty to TARGET_EMAIL, from SENDER
    :param description: the description of the weather
    :param temp: temperature (in Celsius)
    :param humidity: humidity
    """
    # email stuff
    body = f"The weather today isn't too good, expect {description} with an \n" \
           f"average temperature of {temp}°C and {humidity}% humidity \n" \
           f"(information may not be perfect or 100% accurate)"
    message = Mail(from_email=SENDER, to_emails=TARGET_EMAIL,
                   subject=f"Bad weather alert {TODAY.tm_mday}/{TODAY.tm_mon}/{TODAY.tm_year}",
                   plain_text_content=body)
    sg = SendGridAPIClient(EMAIL_API_KEY)
    sg.send(message)


if __name__ == '__main__':
    setup()
    arguments = sys.argv
    if len(arguments) == 3:
        city = arguments[1]
        country = arguments[2]
    else:
        # IO
        city, country = prompt()

    # Alpha 3 is all upper case in the json
    country = country.upper()

    try:
        ALPHA3_TO_ISO[country]
    except KeyError:
        exit("Country invalid")

    response = get_weather_information(city, country)
    if bad_weather(response):
        print("Sending bad weather email...")
        description = response['weather'][0]['description']
        temp = response['main']['temp']
        humidity = response['main']['humidity']
        send_alert_email(description, temp, humidity)


