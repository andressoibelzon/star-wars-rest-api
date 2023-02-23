"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager



app = Flask(__name__)
app.url_map.strict_slashes = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# ENDPOINTS #

@app.route('/user', methods=['GET'])
def handle_hello():

    ## querys o consultas
    users_query = User.query.all()
    results = list(map(lambda item: item.serialize(),users_query))

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "results": results
    }

    return jsonify(response_body), 200


    # obtiene los datos de un SOLO usuario
@app.route('/user/<int:user_id>', methods=['GET'])
def get_info_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    print(user)
    ## querys o consultas

    response_body = {
        "msg": "ok",
        "result": user.serialize()
    }

    return jsonify(response_body), 200


## crear usuario

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.json
   
    user_query = User.query.filter_by(email=request_body["email"]).first()

    if user_query is None:
        user = User(email=request_body["email"], password=request_body["password"])
        db.session.add(user)
        db.session.commit()

        response_body = {
            "msg": "El usuario ha sido creado con exito",
            # "result": user_query.serialize()
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Usuario ya existe"}), 400






# Autentificacion con JWT

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    print(user)
    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)



# Proteger una ruta
# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    print(user)
    return jsonify({"result":user.serialize()}), 200















# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


