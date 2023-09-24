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
        "header": f"Weather in {location_result['addresses'][0]['address']['municipality']}",
        "weather": weather_result["results"][0]["phrase"],
        "city": location_result["addresses"][0]["address"]["municipality"],
        "country": location_result["addresses"][0]["address"]["country"],
        "temperature": weather_result["results"][0]["realFeelTemperature"]["value"]
    }

    return render_template('index.html', data=data)


@app.route('/user_location', methods=['POST'])
def handle_click():
    location = request.form.get('location')
    email = request.form.get('email')
    print(location)
    show_alert = False
    if location != "":
        user_location_url = f"https://atlas.microsoft.com/search/address/json?&" \
                            f"subscription-key=VCjx6AU_MxmuLPOfiXlqcF-M541X48W0IyvzbvMRGCQ&api-version=1.0&" \
                            f"language=en-US&query={location}"
        user_location_response = requests.get(user_location_url, verify=False)
        user_location_result = user_location_response.json()
        user_latitude = user_location_result["results"][0]["position"]["lat"]
        user_longitude = user_location_result["results"][0]["position"]["lon"]
        user_weather_url = "https://atlas.microsoft.com/weather/currentConditions/json?" \
                           f"api-version=1.0&query={user_latitude},{user_longitude}&" \
                           "subscription-key=VCjx6AU_MxmuLPOfiXlqcF-M541X48W0IyvzbvMRGCQ"
        user_weather_response = requests.get(user_weather_url, verify=False)
        user_weather_result = user_weather_response.json()

        data = {
            "header": f"Weather in {user_location_result['results'][0]['address']['municipality']}",
            "weather": user_weather_result["results"][0]["phrase"],
            "temperature": user_weather_result["results"][0]["temperature"]["value"],
            "city": user_location_result["results"][0]["address"]["municipality"],
            "country": user_location_result["results"][0]["address"]["country"]
        }

        return render_template('index.html', data=data)
    else:
        show_alert = True

        data = {
            "header": "Please enter a location before clicking Go.",
            "weather": "N/A",
            "city": "N/A",
            "country": "N/A",
            "temperature": "N/A"
        }
        return render_template('index.html', show_alert=show_alert, data=data)


if __name__ == "__main__":
    app.run()
