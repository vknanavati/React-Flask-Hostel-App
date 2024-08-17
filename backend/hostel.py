import json
from urllib.request import urlopen
from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
options.add_experimental_option("useAutomationExtension", False)
CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
service = Service(executable_path=CHROME_DRIVER_PATH)

browser = webdriver.Chrome(
    options=options,
    service=service,
)
app = Flask(__name__)
CORS(app)


with open("continent_dict.json", encoding="UTF-8") as country_dict:
    country_dict = country_dict.read()

country_dict = json.loads(country_dict)

# decorator that defines a route for handling HTTP requests
# the @app.route decorator specifies which URL paths (routes) should be handled by a particular function # noqa
# the app.route decorator binds a URL route to a view function
# a view function is a function that handles a request and returns a response
# '/get-country' is the URL endpoint that this route will handle.
# this route is responsible for handling requests sent to 'http://localhost:5000/get-country.' # noqa
# when a client makes a request to this URL, Flask will invoke the fnx decorated with @app.route('/get-country') # noqa
#  methods=['POST'] specifies that the route should only handle POST requests


@app.route('/get-country', methods=['POST'])
def get_country():
    # request.json accesses the JSON data sent from the request body
    # it parses the request body as JSON and returns it as a python dictionary data: {'country': 'Canada'} # noqa
    data = request.json
    print(f"data: {data}")
    # data.get('country') retrieves the value associated with the key 'country' from the JSON data # noqa
    country = data.get('country')
    print(f"country from JSON data received from user input: {country}")

    if country:
        continent = get_continent(country)
        if continent:
            city_results = get_cities(country, continent)
            return jsonify({"country": country, "continent": continent, "cities": city_results}) # noqa

    # For demonstration, simply return the received country
    # converts the python data into a JSON formatted string
    # sets the Content-Type header to application/json
    # tells the client that response being returned is in JSON format
    # return jsonify({"message": f"Received country: {country}"})


def get_continent(country):
    # item = value of k:v
    for item in country_dict.values():
        # print(f"\nCountries in continent: {item}\n")
        # element represents the country in the list of countries from dictionary that country variable will be compared against # noqa
        for element in item:
            # country is the user's choice
            if country == element:
                continent = [k for k, v in country_dict.items() if v == item][0] # noqa
                print(f"\nContinent of country: {continent}\n")
                return continent
    return None


city_list = []


def get_cities(country, continent):
    # generates list of cities with hostels in that country
    url = f"https://www.hostelworld.com/st/hostels/{continent}/{country}/"
    print(f"\nURL to be opened: {url}\n")
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()

    browser.get(url)
    # time.sleep(4)

    results = browser.find_elements(
        By.XPATH,
        "//div[@class='average-city-prices-list']/a"
    )

    for result in results:
        title = result.get_attribute("title")
        city_list.append(title)
    print(f"\nList of cities: {city_list}\n")
    # print(*city_list, sep="\n")
    # time.sleep(5)
    # browser.quit()

    return city_list


if __name__ == '__main__':
    app.run(port=5000, debug=True)
