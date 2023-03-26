# Bad weather notifier
Made for the people that leave their house in the morning without an umbrella when it will rain all day long because they didn't check the weather (me) !

## How to set up
- You will need to put your own api credentials in a file called "api-keys.json" for [Open Weather](https://home.openweathermap.org/), 
 and for [SendGrid](https://sendgrid.com/) as well as your sender and target emails under the same directory as the python file, that file should be a json file with
 the following properties:
  - "OpenWeatherKey" for the open weather api key
  - "SendGridKey" for the send grid api key, and
  - "SendGridSender" for the email of the sender
    - For these 2 you need to make and set up a SendGrid account, create a new sender (whose email you will set as the value of the SendGridSender property) and make a new API key with full access then set the value SendGridKey to be that API key 
  - "TargetEmail" for the target email

- You will need to run json-retrieve.sh under bash-scripts to get the required Json files that are needed to run the script

- Finally, you will need to download the lybraries using ```pip install -r requirements.txt```, ideally you would do so in a virtual environment to not mess with your global lybraries

- Once all of that is done, you can run the python script

- Use Windows task scheduler and such to automatically run it once a day

## How to use
### CLI
- You can run the script through the shell this way ```python3 .\weather.py [city-name] [country-alpha-3]```
  - citty-name needs to be capitalized
### IO
 - You can also just run the script directly and input the required information on the go
   - You will first be prompted to input the city name
   - You will then be prompted to input the country name - 
#### In both cases the TargetEmail in the .json you made will receive an email from the SendGridSender email if the weather isn't too good.

## Sources
- ISO 3166 json retrieved from [lukes / ISO-3166-Countries-with-Regional-Codes ](https://github.com/lukes/ISO-3166-Countries-with-Regional-Codes)

