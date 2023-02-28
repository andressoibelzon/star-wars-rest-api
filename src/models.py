from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favoritos = db.relationship('Favoritos',backref='user', lazy=True)
    def _repr_(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "favoritos": self.favoritos,
            # do not serialize the password, its a security breach
        }
        
class Planeta(db.Model):

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    diametro = db.Column(db.String(250), nullable=False)
    periodo_orbital = db.Column(db.String(250), nullable=False)
    poblacion =  db.Column(db.String(250), nullable=False)
    favoritos = db.relationship('Favoritos',backref='planeta', lazy=True)
    
    
    def _repr_(self):
        return '<Planeta %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "periodo_orbital": self.periodo_orbital,
            "poblacion": self.poblacion,
            "favoritos": self.favoritos,
            # do not serialize the password, its a security breach
        }
        
class Personaje(db.Model):
    
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    altura = db.Column(db.String(250), nullable=False)
    genero =  db.Column(db.String(250), nullable=False)
    peso =  db.Column(db.String(250), nullable=False)
    favoritos = db.relationship('Favoritos',backref='personaje', lazy=True)

    
    def _repr_(self):
        return '<Personaje %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "genero": self.genero,
            "peso": self.peso,
            "favoritos": self.favoritos,
            # do not serialize the password, its a security breach
        }
        

        
class Favoritos(db.Model):

    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'))
    personaje_id = db.Column(db.Integer, db.ForeignKey('personaje.id'))
    
    def _repr_(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planeta_id": self.planeta_id,
            "personaje_id": self.personaje_id,

            # do not serialize the password, its a security breach
        }