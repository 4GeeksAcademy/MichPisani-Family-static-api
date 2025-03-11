"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

initial_members =[        
    {
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    },
    {
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    },
    {
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1]
    }]
#Añadir todos los miembros
for member in initial_members:
    jackson_family.add_member(member)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }


    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    response_body = {
        "message": "This is your member",
        "member": member
    }
    return jsonify(member)


@app.route('/member', methods = ['POST'])
def new_member():
    request_body = request.json
    print(request_body)
    new_member={
        "id": request_body["id"],
        "first_name": request_body["first_name"],
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }

    jackson_family.add_member(new_member)
    response_body = {
        "message": "The member was added succesfully"
    }
    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods = ['DELETE'])
def delete_member(id):
    jackson_family.delete_member(id)
    response_body = {
        "done": True
    }
    return jsonify(response_body),200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
