
import os # importing operating system tools
import datetime # importing date and time module
from flask import Flask, render_template , redirect , url_for , flash , request , jsonify # importing flask 
from flask_bootstrap import Bootstrap # importing flask-bootstrap
from werkzeug.security import generate_password_hash , check_password_hash # importing werkzeug tools forsecurity 
from werkzeug.utils import secure_filename # for working should install Werkzeug==0.16.1
from itsdangerous import URLSafeTimedSerializer , SignatureExpired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user # importing flask-login
from flask_mail import Mail , Message 
from forms import * # importing forms



# init flaskapp
app = Flask(__name__)

# init flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'sign_in_page'

# init flask-mail
mail = Mail(app)

# init flask-bootstrap
Bootstrap(app)

# importing models
from models import *

# take cofiguration from config.cfg
app.config.from_pyfile('config.cfg')

# config the secret key for itsdangerous lib with my flask Secret Key
serial = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# Verification of an image extention
def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


# Routes start from here .....

# Home page of storia
@app.route('/')
def home_page():
    title = "Home"
    return render_template('home-page.html' , title=title)


################### The login and logout routes ##############
# login manager 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout route , it will redirect you to the home page after logout 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

###############################################################

# sign-up route and page 
@app.route('/sign-up', methods=['GET' , 'POST'])
def sign_up_page():
    form = RegisterForm()
    time_now = datetime.datetime.now()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data , method='sha256')
        new_user = User(name = form.name.data ,username= form.username.data, email=form.email.data, user_gender = form.gender.data , phone_number = form.phone_number.data 
                        , password=hashed_password , user_role = 'Normale User' , email_confirmation = 'not_confirmed' , profile_created_on = time_now ) 
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('sign_in_page'))
        
    return render_template('sign-up-page.html' , form=form)


# login page and route 
@app.route('/sign-in', methods=['GET' , 'POST'])
def sign_in_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data ).first()
        if user:
            if check_password_hash(user.password , form.password.data):
                login_user(user, remember=form.remember.data)

                if user.email_confirmation == "not_confirmed":

                    email = user.email
                    print (email)
                    token = serial.dumps(email , salt="YwOiqH1tqf")
                    print (token)
                    msg = Message('Confirm Email' , sender='previewsites40@gmail.com' , recipients=[email])
                    
                    link = url_for('confirme_email' , token=token , _external=True )

                    msg.body = '<h1>Your confirmation link is <a>{}</a> </h1> '.format(link)
                    print (msg.body)

                    mail.send(msg)
                    print('Email sent')

                    return render_template('email-confirmation.html')
                
                return redirect(url_for('profile'))
            else:
                flash('Password incorrect !')
                return redirect(url_for('sign_in_page'))  
        
        if not user:
            flash('Username incorrect !')
            return redirect(url_for('sign_in_page'))

    return render_template('sign-in-page.html', form=form)


# confirme email
@login_required
@app.route('/confirme_email/<token>')
def confirme_email(token):
    user = User.query.filter_by(username = current_user.username ).first()

    try:
        email = serial.loads(token , salt='YwOiqH1tqf' , max_age=360)
        user.email_confirmation = "confirmed"
        db.session.commit()

        return redirect(url_for('profile'))

    except SignatureExpired:

        return '<h1> The token is expired </h1>'

    return '<h1> The token works fine {} </h1>'.format(token)

####################### Profiling ########################

# profile route .... 
@app.route('/profile' , methods=['GET' , 'POST'])
@login_required
def profile():
    title = "Profile"
    user = User.query.filter_by(username = current_user.username ).first()
    

    if request.method == "POST" :

        if request.files : 
            image = request.files["image"]

            if image.filename == "":
                
                return redirect(request.url)

            # check the allowed image extentions 
            if allowed_image(image.filename):
                
                filename = secure_filename(image.filename) 

                # saving the image into our path
                image.save(os.path.join(app.config['IMAGE_UPLOADS'] , image.filename ))

                # rename the image 
                img_ext = (image.filename).rsplit('.' , 1)[1]
                newImageName =  user.username + '.' + img_ext

                path = app.config['IMAGE_UPLOADS'] + '/'

                newImageFileName = os.rename(path + image.filename , path + newImageName)

                

                user.image_profile_name = newImageName
                db.session.commit()
                

            flash('Image uploaded succeful ! (refresh page to see it)')

            return redirect(url_for('profile'))
            
 
    return render_template('profile.html',  username_view=current_user.username, user=user , title=title)

#############################################################

# dashboard route .... that only for admin... 
@app.route('/dashboard')
@login_required
def dashboard():
    title = "Dashboard"
    user = User.query.filter_by(username = current_user.username ).first()

    if user.user_role == 'Admin' :
        return render_template('dashboard.html', username_view=current_user.username, user = user , title=title)
    else:
        return redirect(url_for('addstore'))


# store manager  route .... that only for admin...
@app.route('/storemanager')
def storemanager():
    title = "Store Manager"
    stores = Store.query.all()
    stores_lenght = len(stores)
    user = User.query.filter_by(username = current_user.username ).first()

    if user.user_role == 'Admin' :
        return render_template('storemanager.html',  stores_lenght=stores_lenght , username_view=current_user.username ,  user=user , stores=stores , title=title)
    else:
        return redirect(url_for('addstore'))


# adding store  ...
@app.route('/addstore' , methods=['GET' , 'POST'])
@login_required
def addstore():
    title = "Add Store"

    user = User.query.filter_by(username = current_user.username ).first()
    form = Adding_new_store()

    form.store_country.choices = [(country.country_name , country.country_name) for country in Country.query.all()]
    form.store_town.choices = [(town.town_name , town.town_name) for town in Town.query.filter_by(town_from = 'Algeria').all()]
    form.store_province.choices = [(province.province_name , province.province_name) for province in Province.query.filter_by(province_from = 'Mostaganem').all()]


    if form.validate_on_submit():


        # check if the post request has the files part
        files = request.files.getlist('files[]')
        
        newpath = app.config['IMAGE_UPLOADS'] + '/'+ str(form.store_phone.data)
            
        for file in files:
            if file and allowed_image(file.filename):
                filename = secure_filename(file.filename)
                
                if not os.path.exists(newpath):
                    os.makedirs(newpath)

                file.save(os.path.join(newpath, filename))
        
        new_store = Store(store_added_by = current_user.username ,
                            store_owner_name = form.store_owner_name.data ,
                            store_name = form.store_name.data.lower() ,
                            store_categorie = form.store_categories.data , 
                            store_phone_number = form.store_phone.data ,
                            store_country = form.store_country.data,
                            store_town = form.store_town.data , 
                            store_province = form.store_province.data ,
                            store_position = form.store_position.data ,
                            store_description = form.store_description.data , 
                            store_tags = form.store_tags.data,
                            store_picture = form.store_phone.data
                         )

        db.session.add(new_store)
        db.session.commit()         
        
                    
        flash('Your store was added succcefully !')
        
        if user.user_role == 'Admin' :

            return redirect(url_for('storemanager'))

        else :
            
            return redirect(url_for('addstore'))
       
    
    return render_template('addstore.html', username_view=current_user.username , user=user , form=form ,title=title)


# for all users
# storia route and user home ..... 
@app.route('/storia' , methods=['GET' , 'POST'])
def storia():
    title = "Storia"
    form = Searching_barre_form()
    stores = Store.query.all()

    if form.validate_on_submit() :

        x = '00'

        if form.store_categories.data == x :
            
            stores = Store.query.whooshee_search(str(form.search_barr.data)).all()

            print(stores)


        return render_template('storia.html' , stores = stores  ,title=title , form = form)
        

    return render_template('storia.html', stores = stores  ,title=title , form = form )

# store route 
@app.route('/store/<storename>' , methods=['GET' , 'POST'])
def store(storename):
    title = "Store"
    stores = Store.query.filter_by(store_name = storename).all()
    mypath = os.listdir('static/uploads/images/' + str([store.store_phone_number for store in stores][0]))
    print(mypath)

    for store in stores : 
       x =  store.store_position
       position = x.split()


    return render_template('store.html' , stores=stores , mypath=mypath , position=position , title = title)

# ============== Routes that retorn json data =========
# get selected Towns route for jsonfiy
@app.route('/api_v1/getTowns/<townname>')
@login_required
def getTowns(townname):
    provinces = Province.query.filter_by(province_from=townname).all()
    

    positionArray = []

    for province in provinces :
        provinceObj = {}
        provinceObj['Town'] = province.province_from
        provinceObj['Province'] = province.province_name
        provinceObj['Postal_code'] = province.province_postal_code
        positionArray.append(provinceObj)

    return jsonify({'position': positionArray})


# get selected Countries route for jsonfiy
@app.route('/api_v1/getCountries/<countryname>')
@login_required
def getCountries(countryname):
    countries= Town.query.filter_by(town_from=countryname).all()
    

    positionArray = []

    for country in countries :
        countryObj = {}
        countryObj['Country'] = country.town_from
        countryObj['Town'] = country.town_name
        countryObj['Postal_code'] = country.town_postal_code
        positionArray.append(countryObj)

    return jsonify({'position': positionArray})

# =====================================================

# testing routes
@app.route('/mappingtest' , methods=['GET' , 'POST'])
def mappingtest():
    title = "Mapping Test"

    """
    store = Store.query.filter_by(store_name = "alfe mall").first()

    db.session.delete(store)
    db.session.commit()
    """

    if request.method == 'POST':
            # check if the post request has the files part
            files = request.files.getlist('files[]')
            print(files)
            
            for file in files:
                if file and allowed_image(file.filename):
                    filename = secure_filename(file.filename)
                    newpath = app.config['IMAGE_UPLOADS'] + '/storia'

                    if not os.path.exists(newpath):
                        os.makedirs(newpath)

                    file.save(os.path.join(newpath, filename))

                    

            
            return redirect(request.url)
    
  
    return render_template('mappingtest.html', title=title)





