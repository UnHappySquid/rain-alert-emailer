import requests
import sys
import json


def setup():
    """
    Sets up global variables
    :return: None
    """
    global COUNTRY_TO_ISO, COUNTRY_TO_CITY, API_CREDS
    # This program uses https://openweathermap.org/ for requests, need to set your own api key and
    # write api key info in a file called api-key.txt
    with open("api-key.txt", "r") as creds:
        API_CREDS = creds.read()
    # gets Country to ISO mapping
    with open("data/iso-3166-code.json") as iso:
        json_file_content = iso.read()
        raw_json = json.loads(json_file_content)
        COUNTRY_TO_ISO = {}
        for att in raw_json:
            COUNTRY_TO_ISO[att["name"]] = att["country-code"]
    # gets list of cities for each country
    with open("data/cities.json") as cities:
        content = cities.read()
        COUNTRY_TO_CITY = json.loads(content)


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
    country = input("Input country : ")
    return (city, country)


def get_lat_lon(city, country):
    """
    Fetches the city, country's latitude and longitude.
    :param city: city whose latitude, longitude we want
    :param country: the country of that city
    :return: a tuple of the latitude and longitude
    """
    country_iso = COUNTRY_TO_ISO[country]
    response = requests\
        .get(f"https://api.openweathermap.org/data/2.5/weather?"
             f"q={city},{country_iso}&appid={API_CREDS}&units=metric")
    api_response = response.json()
    print(api_response)
    lat = api_response["coord"]["lat"]
    lon = api_response["coord"]["lon"]
    return lat, lon


if __name__ == '__main__':
    setup()
    city, country = prompt()

    try:
        COUNTRY_TO_ISO[country]
    except KeyError:
        exit("Country invalid")

    if city not in COUNTRY_TO_CITY[country]:
        exit("City invalid")

    lat, lon = get_lat_lon(city, country)

