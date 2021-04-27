# Storia

> Easy way to find Stores (Storia make you shopping easier)
> > A smaill project i was working on 2 years ago, i am sharing that just for learning purpose. 

> Open cinfig.cfg and put your keys here:
`# google recaptcha config`
`RECAPTCHA_PUBLIC_KEY= YOUR KEY HERE`
`RECAPTCHA_PRIVATE_KEY= YOUR KEY HERE`

`# config app and googlemaps`
`GOOGLEMAPS_KEY = YOUR KEY HERE`

## Run

1- activate the vertual env: </br>
linux: `source venv/bin/activate`

2- install the requirments: </br>
`pip install requirements.txt`

3- run the flask server: </br>
`python3 run_app.py`

4- create the database: </br>
`python3`
`from app import db`
`db.create.all()`

## Screenshots

![Example screenshot](./screenshoots/search.png)
![Example screenshot](./screenshoots/home.png)
![Example screenshot](./screenshoots/profile.png)
![Example screenshot](./screenshoots/add-store.png)
