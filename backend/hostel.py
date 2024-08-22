import json
import re
import subprocess
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__, static_folder='static')
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
    # data.get('country') retrieves the value associated with the key 'country' # noqa
    country = data.get('country').capitalize()
    print(f"country from user input: {country}")

    # get_continent uses the country variable to get the continent
    continent = get_continent(country)
    if not continent:
        return jsonify({"error": "Invalid country name. Please check your input."}), 400 # noqa
    # city_results uses the country and continent variables to call hostel world website # noqa
    city_results = get_cities(country, continent)

    # jsonify is a Flask function that converts the python dictionary into a JSON-formatted string (JSON object) # noqa
    # it also sets the 'Content-Type' header of the response to 'application/json' this tells the client that the content being returned is in JSON format # noqa
    # jsonify returns a Flask response object that contains the JSON data and appropriate headers # noqa
    return jsonify({"country": country, "continent": continent, "cities": city_results}) # noqa


def get_continent(country):
    # item = value of k:v
    for item in country_dict.values():
        # element represents the country in the list of countries from dictionary that country variable will be compared against # noqa
        for element in item:
            # country is the user's choice
            if country == element:
                continent = [k for k, v in country_dict.items() if v == item][0] # noqa
                print(f"\nContinent of country: {continent}\n")
                return continent
    return None


def get_cities(country, continent):
    city_list = []
    # generates list of cities with hostels in that country
    url = f"https://www.hostelworld.com/st/hostels/{continent}/{country}/"
    print(f"\nURL to be opened: {url}\n")

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    parent_div = soup.find("div", class_="average-city-prices-list")

    city_links = parent_div.find_all("a")

    for link in city_links:
        title = link.get("title")
        city_list.append(title)

    print(f"\nList of cities: {city_list}\n")

    return city_list


@app.route('/get-user-city', methods=['POST'])
def get_user_city():
    data = request.json
    #  {'country': 'England', 'continent': 'europe', 'city': 'London'}
    print(f"\nData received from client after user selected city: {data}\n")

    country = data.get('country')
    continent = data.get('continent')
    city = data.get('city')

    paginated_list = city_page(continent, country, city)
    hostels_links = links_city_hostels(paginated_list)
    city_ratings_dict = city_hostel_dict(hostels_links)

    df = pd.DataFrame(city_ratings_dict)
    # print(df)
    df.to_csv("Hostel_City_Ratings.csv")
    print("\nCSV created! YAY!!\n")

    try:
        subprocess.run([
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "hostel_graphs.ipynb"
        ], check=True)
        print("Notebook ran succesfully")
    except subprocess.CalledProcessError as e:
        print(f"Notebook error {e}")

    if not data:
        return jsonify({"error": "no data received"}), 400

    if not city:
        return jsonify({"error": "no city received"}), 400

    result = {"city": city}
    return jsonify(result), 200


def city_page(continent, country, city):
    url = f"https://www.hostelworld.com/st/hostels/{continent}/{country}/{city}/" # noqa
    # replaces any white space with %20
    url = url.replace(" ", "%20")
    print(url)

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    pagination_section = soup.find("section", {"name": "pagination"})

    if pagination_section:
        print("\nDetected pagination.\n")

        raw_string = pagination_section.get_text(separator="").replace("\n", "") # noqa
        digit_string = re.sub("[^0-9]", "", raw_string)
        # digit_list = number of pages ex. London has 4 pages worth of hostels
        # so digit_list = [1, 2, 3, 4]
        digit_list = [int(page) for page in digit_string]

        print("\nDetermined number of pages.\n")
        print(f"\ndigit_list is: {digit_list}\n")

        # url_list initially creates template hostel link for each element in digit list # noqa

        url_list = [url for count in enumerate(digit_list)]

        # page number syntax is added to [1:]
        # url_list: [
        #   'https://www.hostelworld.com/st/hostels/europe/england/london/',
        #   'https://www.hostelworld.com/st/hostels/europe/england/london/p/2/',
        #   'https://www.hostelworld.com/st/hostels/europe/england/london/p/3/',
        #   'https://www.hostelworld.com/st/hostels/europe/england/london/p/4/'
        # ]
        i = 1
        for index, dummy in enumerate(url_list):
            i = i + 1
            url_list[index] = url_list[index] + "/p/" + str(i) + "/"

        print(f"Paginated url list: {url_list}")
        return url_list
    else:
        print("\nThis city has only one page worth of hostels.\n")
        url_list = [url]
        print(f"Single url link: {url_list}")
        return url_list


links_list = []


def links_city_hostels(paginated_list):

    for index, dummy in enumerate(paginated_list):
        page = requests.get(paginated_list[index], timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        link_elements = soup.find_all("div", class_="property-listing-cards")
        # scrape each page for links for each hostel listed
        for link in link_elements:
            results = link.find_all("a")
            for result in results:
                link_url = result["href"]
                links_list.append(link_url)

    url_count = len(links_list)
    print(f"\nlinks_list = {links_list}\n")
    print(f"\nLength of list: {url_count}")
    return url_count


def city_hostel_dict(hostels_links):
    name_list = []
    composite_hostel_scores = []

    for url in range(0, hostels_links):
        page = requests.get(links_list[url], timeout=10)

        soup = BeautifulSoup(page.text, "html.parser")

        hostel_name = soup.find("h1").text.strip()
        name_list.append(hostel_name)

        parent_divs = soup.find_all('div', class_='rating-label-score-wrapper')

        specific_scores = [
            parent_div.find('div', class_='rating-score').text.strip() for
            parent_div in parent_divs
        ]

        composite_hostel_scores.append(specific_scores)

        lists_to_join = zip(name_list, composite_hostel_scores)
        specific_ratings = list(lists_to_join)
        # print(f"\nSpecific ratings: {specific_ratings}\n")
        ratings_dict = dict(specific_ratings)

        dict_length = len(ratings_dict)

        print(f"\nProgress: {dict_length}/{hostels_links} ")

    no_ratings_dict = {key: value for (key, value) in ratings_dict.items() if not value} # noqa

    ratings_dict = {key: value for (key, value) in ratings_dict.items() if value} # noqa

    no_rating_list = list(no_ratings_dict.keys())
    no_rating_string = ", ".join([str(elem) for elem in no_rating_list])

    print(f"\nComplete Dictionary: {ratings_dict}\n")
    print(f"Unrated hostels: {no_rating_string}")
    return ratings_dict


if __name__ == '__main__':
    app.run(port=5000, debug=True)
