from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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

    # For demonstration, simply return the received country
    # converts the python data into a JSON formatted string
    # sets the Content-Type header to application/json
    # tells the client that response being returned is in JSON format
    return jsonify({"message": f"Received country: {country}"})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
