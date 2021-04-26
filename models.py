# models.py
from app import app # import flask application from app.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_whooshee import Whooshee


# init flask-sqlalchemy
db = SQLAlchemy(app)

# init flask_whoshee
whooshee = Whooshee(app)

# SqlAlchemy models tabels 

# user table 
class User(UserMixin , db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))
    user_gender = db.Column(db.String(15))
    image_profile_name =  db.Column(db.String(500))
    phone_number = db.Column(db.Integer , unique=True)
    user_role = db.Column(db.String(15))
    email_confirmation = db.Column(db.String(15))
    profile_created_on = db.Column(db.String(30))



# whooshee indexing for stores tabels
@whooshee.register_model('store_name' , 'store_categorie' , 'store_tags')

# store table
class Store(db.Model): 
    __tablenmae__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    store_added_by = db.Column(db.String(100))
    store_owner_name = db.Column(db.String(100))
    store_name = db.Column(db.String(100))
    store_categorie = db.Column(db.String(100))
    store_phone_number = db.Column(db.Integer, unique=True)
    store_position = db.Column(db.String(100), unique=True)
    store_country = db.Column(db.String(100))
    store_town = db.Column(db.String(100))
    store_province = db.Column(db.String(100))
    store_description = db.Column(db.String(100))
    store_tags = db.Column(db.String(100))
    store_picture = db.Column(db.String(500))
    

    def __init__(self ,store_added_by ,store_owner_name ,store_name ,store_categorie ,store_phone_number ,store_position ,store_town ,store_province ,store_description ,store_tags ,store_country ,store_picture):
 
        self.store_added_by = store_added_by
        self.store_owner_name = store_owner_name
        self.store_name = store_name
        self.store_categorie = store_categorie
        self.store_phone_number = store_phone_number
        self.store_position = store_position
        self.store_town = store_town
        self.store_province = store_province
        self.store_description = store_description
        self.store_tags = store_tags
        self.store_country = store_country
        self.store_picture = store_picture


# country table
class Country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer,primary_key=True)
    country_name = db.Column(db.String(100),unique=True)
    country_code = db.Column(db.String(50),unique=True)
    country_phone_code = db.Column(db.Integer,unique=True)
    country_currency = db.Column(db.String(50))

# town table
class Town(db.Model):
    __tablename__ = 'town'

    id = db.Column(db.Integer,primary_key=True)
    town_from = db.Column(db.String(100))
    town_postal_code = db.Column(db.Integer, unique=True)
    town_name = db.Column(db.String(100),unique=True)

# province table
class Province(db.Model):
    __tablename__ = 'province'

    id = db.Column(db.Integer,primary_key=True)
    province_from = db.Column(db.String(100),unique=True)
    province_postal_code = db.Column(db.Integer, unique=True)
    province_name = db.Column(db.String(100),unique=True)
