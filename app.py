from flask import Flask, render_template, request
import requests
app = Flask(__name__)


@app.route('/')
def get_location():
    weather_url = "https://atlas.microsoft.com/weather/currentConditions/json?" \
                  f"api-version=1.0&query=47.60357,-122.32945&" \
                  "subscription-key=VCjx6AU_MxmuLPOfiXlqcF-M541X48W0IyvzbvMRGCQ"
    location_url = "https://atlas.microsoft.com/search/address/reverse/json?" \
                   f"api-version=1.0&query=47.60357,-122.32945&" \
                   "subscription-key=VCjx6AU_MxmuLPOfiXlqcF-M541X48W0IyvzbvMRGCQ"
    weather_response = requests.get(weather_url, verify=False)
    location_response = requests.get(location_url, verify=False)
    weather_result = weather_response.json()
    location_result = location_response.json()

    data = {
        "weather": weather_result["results"][0]["phrase"],
        "city": location_result["addresses"][0]["address"]["municipality"],
        "country": location_result["addresses"][0]["address"]["country"],
        "temperature": weather_result["results"][0]["realFeelTemperature"]["value"]
    }

    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run()
