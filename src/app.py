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
from models import db, User, Planeta, Personaje, Favoritos
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


############ USER 
@app.route('/user', methods=['GET'])
def get_all_users():

    ## querys o consultas
    users_query = User.query.all()
    results = list(map(lambda item: item.serialize(),users_query))

    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "result": results
    }

    return jsonify(response_body), 200


    # obtiene los datos de un SOLO usuario
@app.route('/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    print(user)
    ## querys o consultas

    response_body = {
        "msg": "ok",
        "result": user.serialize()
    }

    return jsonify(response_body), 200


    # CREAR USUARIO

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
            "result": user_query.serialize()
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Usuario ya existe"}), 400


############ PLANETAS

# OBTENER TODOS LOS PLANETAS
@app.route('/planeta', methods=['GET'])
def get_all_planetas():

    ## querys o consultas
    planetas_query = Planeta.query.all()
    results = list(map(lambda item: item.serialize(),planetas_query))

    response_body = {
        "msg": "Hello, this is your GET /planetas response ",
        "result": results
    }

    return jsonify(response_body), 200

# OBTENER UN PLANETA
@app.route('/planeta/<int:planeta_id>', methods=['GET'])
def get_one_planeta(planeta_id):
    planeta = Planeta.query.filter_by(id=planeta_id).first()
    print(planeta)
    ## querys o consultas

    response_body = {
        "msg": "ok",
        "result": planeta.serialize()
    }

    return jsonify(response_body), 200

# CREAR PLANETA
@app.route('/planeta', methods=['POST'])
def create_planeta():
    request_body = request.json

    planeta_query = Planeta.query.filter_by(nombre=request_body["nombre"]).first()
    print(planeta_query)

    if planeta_query is None:
        planeta = Planeta(nombre=request_body["nombre"], diametro=request_body["diametro"], periodo_orbital=request_body["periodo_orbital"], poblacion=request_body["poblacion"])
        db.session.add(planeta)
        db.session.commit()
        print(planeta)

        response_body = {
            "msg": "El planeta ha sido creado con exito",
            "result": planeta.serialize()
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Planeta ya existe"}), 400


############ PERSONAJES

# OBTENER TODOS LOS PERSONAJES
@app.route('/personaje', methods=['GET'])
def get_all_personajes():

    ## querys o consultas
    personajes_query = Personaje.query.all()
    results = list(map(lambda item: item.serialize(),personajes_query))

    response_body = {
        "msg": "Hello, this is your GET /personajes response ",
        "result": results
    }

    return jsonify(response_body), 200


    # OBTENER UN PERSONAJE
@app.route('/personaje/<int:personaje_id>', methods=['GET'])
def get_one_personaje(personaje_id):
        personaje = Personaje.query.filter_by(id=personaje_id).first()
        print(personaje)
        ## querys o consultas

        response_body = {
            "msg": "ok",
            "result": personaje.serialize()
        }

        return jsonify(response_body), 200


        # CREAR PERSONAJE
@app.route('/personaje', methods=['POST'])
def create_personaje():
    request_body = request.json

    personaje_query = Personaje.query.filter_by(nombre=request_body["nombre"]).first()
    print(personaje_query)

    if personaje_query is None:
        personaje = Personaje(nombre=request_body["nombre"], altura=request_body["altura"], genero=request_body["genero"], peso=request_body["peso"])
        db.session.add(personaje)
        db.session.commit()
        print(personaje)

        response_body = {
            "msg": "El personaje ha sido creado con exito",
            "result": personaje.serialize()
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Personaje ya existe"}), 400



############ FAVORITOS

    # OBTENER TODOS LOS FAVORITOS
@app.route('/favoritos', methods=['GET'])
def get_all_favoritos():

    ## querys o consultas
    favoritos_query = Favoritos.query.all()
    results = list(map(lambda item: item.serialize(),favoritos_query))

    response_body = {
        "msg": "Hello, this is your GET /favoritos response ",
        "result": results
    }

    return jsonify(response_body), 200


    # OBTENER UN FAVORITO
@app.route('/favoritos/<int:favoritos_id>', methods=['GET'])
def get_one_favorito(favoritos_id):
        favorito = Favoritos.query.filter_by(id=favoritos_id).first()
        print(favorito)
        ## querys o consultas

        response_body = {
            "msg": "ok",
            "result": favorito.serialize()
        }

        return jsonify(response_body), 200


        # CREAR FAVORITO PLANETA
@app.route('/favoritos/planeta', methods=['POST'])
def create_favorito_planetas():
    request_body = request.json

    favorito_query = Favoritos.query.filter_by(user_id=request_body["user_id"]).first()
    print(favorito_query)

    if favorito_query is None:
        favorito = Favoritos(user_id=request_body["user_id"], planeta_id=request_body["planeta_id"])
        db.session.add(favorito)
        db.session.commit()
        print(favorito)

        response_body = {
            "msg": "El favorito de planeta ha sido creado con exito",
            # "result": personaje.serialize()
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Favorito ya existe"}), 400


# CREAR FAVORITO PERSONAJES
@app.route('/favoritos/personaje', methods=['POST'])
def create_favorito_personajes():
    request_body = request.json

    favorito_query = Favoritos.query.filter_by(user_id=request_body["user_id"]).first()
    print(favorito_query)

    if favorito_query is None:
        favorito = Favoritos(user_id=request_body["user_id"], personaje_id=request_body["personaje_id"])
        db.session.add(favorito)
        db.session.commit()
        print(favorito)

        response_body = {
            "msg": "El favorito de personaje ha sido creado con exito",
            # "result": personaje.serialize()
        }

        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Favorito ya existe"}), 400


# , personaje_id=request_body["personaje_id"]



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


