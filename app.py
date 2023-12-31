import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests

load_dotenv()
keyVaultName = os.getenv("AZ_KEYVAULT_NAME")
client_id = os.getenv("AZURE_CLIENT_ID")
tenant_id = os.getenv("AZURE_TENANT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")

app = Flask(__name__)
kvUri = f"https://{keyVaultName}.vault.azure.net"
credential = ClientSecretCredential(
    client_id=client_id,
    client_secret=client_secret,
    tenant_id=tenant_id
)
client = SecretClient(vault_url=kvUri, credential=credential)
azMapKey = client.get_secret("map-key")
print(azMapKey.value)
weather_url = "https://atlas.microsoft.com/weather/currentConditions/json?" \
              f"api-version=1.0&query=47.60357,-122.32945&" \
              f"subscription-key={azMapKey.value}"
location_url = "https://atlas.microsoft.com/search/address/reverse/json?" \
               f"api-version=1.0&query=47.60357,-122.32945&" \
               f"subscription-key={azMapKey.value}"
weather_response = requests.get(weather_url, verify=False)
location_response = requests.get(location_url, verify=False)
weather_result = weather_response.json()
location_result = location_response.json()

sample_city = location_result['addresses'][0]['address']['municipality']
sample_weather = weather_result["results"][0]["phrase"]
sample_temperature = weather_result["results"][0]["realFeelTemperature"]["value"]
sample_country = location_result["addresses"][0]["address"]["country"]


@app.route('/')
def get_location():
    data = {
        "header": f"Weather in {sample_city}",
        "weather": sample_weather,
        "city": sample_city,
        "country": sample_country,
        "temperature": sample_temperature
    }

    return render_template('index.html', data=data)


@app.route('/user_location', methods=['POST'])
def handle_click():
    location = request.form.get('location')
    email = request.form.get('email')
    checkbox = request.form.get('checkbox')
    if checkbox and not email:
        data = {
            "header": f"Weather in {sample_city}",
            "weather": sample_weather,
            "city": sample_city,
            "country": sample_country,
            "temperature": sample_temperature
        }
        error = "Please enter your email to subscribe to alerts!"
        return render_template('index.html', data=data, error=error)

    if not location:
        data = {
            "header": f"Weather in {sample_city}",
            "weather": sample_weather,
            "city": sample_city,
            "country": sample_country,
            "temperature": sample_temperature
        }
        error = "Please enter a location before clicking Go!"
        return render_template('index.html', data=data, error=error)

    user_location_url = f"https://atlas.microsoft.com/search/address/json?&" \
                        f"subscription-key={azMapKey.value}&api-version=1.0&" \
                        f"language=en-US&query={location}"
    user_location_response = requests.get(user_location_url, verify=False)
    user_location_result = user_location_response.json()
    user_latitude = user_location_result["results"][0]["position"]["lat"]
    user_longitude = user_location_result["results"][0]["position"]["lon"]
    user_weather_url = "https://atlas.microsoft.com/weather/currentConditions/json?" \
                       f"api-version=1.0&query={user_latitude},{user_longitude}&" \
                       f"subscription-key={azMapKey.value}"
    user_weather_response = requests.get(user_weather_url, verify=False)
    user_weather_result = user_weather_response.json()

    data = {
        "header": f"Weather in {user_location_result['results'][0]['address']['municipality']}",
        "weather": user_weather_result["results"][0]["phrase"],
        "temperature": user_weather_result["results"][0]["temperature"]["value"],
        "city": user_location_result["results"][0]["address"]["municipality"],
        "country": user_location_result["results"][0]["address"]["country"]
    }

    msg = ""
    if checkbox and email:
        function_url = os.getenv("FUNCTION_URL")
        func_body = {"email": email}
        func_response = requests.get(function_url, json=func_body)
        ack = func_response.json()
        print(ack['message'])
        if ack['message'] == "success":
            msg = "You have successfully subscribed to weather alerts!"
        elif ack['message'] == "failed":
            msg = "Something went wrong."
    return render_template('index.html', data=data, message=msg)


if __name__ == "__main__":
    app.run()
