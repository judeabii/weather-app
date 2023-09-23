from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def get_location():

    data = {
        "weather": "Rain",
        "city": "Bangalore",
        "country": "India",
        "temperature": "21",
    }

    return render_template('index.html', data=data)


if __name__ == "__main__":
    app.run()
