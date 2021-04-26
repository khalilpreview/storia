# formes.py
from flask_wtf import FlaskForm , RecaptchaField 
from wtforms import StringField, PasswordField , BooleanField , TextAreaField , FormField , IntegerField , SelectField , SubmitField , FileField
from wtforms.validators import InputRequired , Email , Length 
from flask_wtf.file import  FileRequired


#Flask_wtf Forms 

# registration form
class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid E-mail'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=15)])
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=50)])
    gender = SelectField(u'gender', choices=[('Man', 'Man') ,('Women', 'Women') ])
    phone_number = StringField('Phone number' , validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    #recaptcha = RecaptchaField()


# login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')
    #recaptcha = RecaptchaField()


# adding new store form 
class Adding_new_store(FlaskForm):

    store_owner_name = StringField('Owner complet name', validators=[InputRequired(), Length(min=3, max=30)])
    store_name = StringField('Store name', validators=[InputRequired(), Length(min=3, max=30)])
    store_categories = SelectField(u'Store Ctégorie', choices=[('00', 'Catégorie'), ('Supérette', 'Supérette'),('Boucherie', 'Boucherie'), ('Bijouterie', 'Bijouterie'), ('Fleuriste', 'Fleuriste'), ('Centre commercial, Centre commercial |', ' Centre commercial, centre commercial '), (' Coiffeur, coiffeur ',' Coiffeur, coiffeur '), (' Opticien ',' Opticien '), (' Épicier ',' Épicier '), (' Agence de voyages ',' Agence de voyages '), (' Magasin de jouets ',' Magasin de jouets '), (' Magasin de musique ',' Magasin de musique '), (' Magasin de chaussures ',' Magasin de chaussures '), (' Magasin de vêtements ',' Magasin de vêtements ') , ('Quincaillerie', 'Quincaillerie'), ('Restaurant', 'Restaurant'), ('Fast Food', 'Fast Food'),('Station essence' , 'Station essence'), ('Tabac et cosmétique', 'Tabac et cosmétique')])
    store_phone = IntegerField('Phone number', validators=[InputRequired()])
    store_position = StringField('Position', validators=[InputRequired()])
    store_country = SelectField(u'Country', choices=[])
    store_town = SelectField(u'Town', choices=[])
    store_province = SelectField(u'Province', choices=[])
    store_description = StringField('Welcome message', validators=[InputRequired()])
    store_tags = TextAreaField(validators=[InputRequired()])
    
   


# searching form 
class Searching_barre_form(FlaskForm):
    search_barr = StringField( '',validators=[InputRequired(), Length(min=3, max=50)])
    store_categories = SelectField(u'' ,choices=[('00', 'Catégorie'), ('Supérette', 'Supérette'),('Boucherie', 'Boucherie'), ('Bijouterie', 'Bijouterie'), ('Fleuriste', 'Fleuriste'), ('Centre commercial, Centre commercial |', ' Centre commercial, centre commercial '), (' Coiffeur, coiffeur ',' Coiffeur, coiffeur '), (' Opticien ',' Opticien '), (' Épicier ',' Épicier '), (' Agence de voyages ',' Agence de voyages '), (' Magasin de jouets ',' Magasin de jouets '), (' Magasin de musique ',' Magasin de musique '), (' Magasin de chaussures ',' Magasin de chaussures '), (' Magasin de vêtements ',' Magasin de vêtements ') , ('Quincaillerie', 'Quincaillerie'), ('Restaurant', 'Restaurant'), ('Fast Food', 'Fast Food'),('Station essence' , 'Station essence'), ('Tabac et cosmétique', 'Tabac et cosmétique')])
    submit = SubmitField('Search')


