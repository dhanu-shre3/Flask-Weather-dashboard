import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__) #during run time name gets replaced to the name of the file

#when we open a page(route) or this /, we want the user to see a simple homepage with weather report
@app.route('/')
def weather_dashboard():
    return render_template("home.html")

@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    
    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
#formating the float value of temp to 2 decimal places only
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    #weather in json file is an array that has the dictionary. [0]accesses the first element in the array that is the dictionary values, then the key value-main
    location = data["name"]
#key values that we want to render to the user
    return render_template('results.html', 
                           location=location, temp=temp, 
                           feels_like=feels_like, weather=weather)






# ini files are easy way to store configurations
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, country_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={},{}&units=metric&appid={}".format(zip_code, country_code, api_key)
    #&units=metric to get degree in celcius and 7units=imperial to get degree in Fahrenheit
    r = requests.get(api_url)
    return r.json()

print(get_weather_results("CF24","GB", get_api_key())  )
#country code for the UK is GB
#Postcode= CF24,GB

if __name__ == '__main__':
    app.run()    
