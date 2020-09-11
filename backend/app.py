from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})

@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)
# Old implementation of /restaurants

# @app.route("/restaurants", methods=['GET'])
# def get_all_restaurants():
#     return create_response({"restaurants": db.get('restaurants')})

@app.route("/restaurants/<id>", methods=['DELETE'])
def delete_restaurant(id):
    if db.getById('restaurants', int(id)) is None:
        return create_response(status=404, message="No restaurant with this id exists")
    db.deleteById('restaurants', int(id))
    return create_response(message="Restaurant deleted")


# TODO: Implement the rest of the API here!

# @route   GET /restaurants/<id>/
# @desc    Returns restaurant with specified id
@app.route("/restaurants/<id>", methods=['GET'])
def get_restaurant(id):
  restaurant = db.getById('restaurants', int(id))
  if restaurant is None:
    return create_response(status=404, message="No restaurant with this id exists")
  return create_response(restaurant)
  
# @route1   GET /restaurants
# @desc1    Returns all restaurants

# @route2   GET /restaurants?minRating=<someNumber>
# @desc2   Returns all restaurants that have a rating that is  minRating or higher

@ app.route("/restaurants", methods=['GET'])
def get_all_restaurants():
    restaurants = db.get('restaurants')
    minRating = request.args.get('minRating')
    if minRating == None: # if there is no query string parameter
      return create_response({"restaurants": db.get('restaurants')}) #list all resturants
    filtered_restaurants = []

    for i in range(0,len(restaurants)): # iterate through restaurants and append to array if the restaurant's rating is greater than or equal to the minRating                       
     if restaurants[i]['rating'] >= int(minRating): 
        filtered_restaurants.append(restaurants[i])

    if len(filtered_restaurants) == 0: # if there are no such resturants with a rating greater than or equal to the minRating 
      return create_response(status=404, message="No restaurants with a rating greater than or equal to the given rating exist")
    return create_response({"restaurants": filtered_restaurants})

# @route   POST /restaurants
# @desc    Adds new restaurant

@app.route("/restaurants", methods=['POST'])
def add_a_restaurant():
  try:
    newRestaurant = {
    'name': request.json['name'],
    'rating': request.json['rating']}
  except KeyError:
    return create_response(status=422, message="Body parameters do not contain both name and rating. Please try again.")
  
  db.create('restaurants',newRestaurant) 
  return create_response({"restaurant": newRestaurant},status=201) 
  



"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
