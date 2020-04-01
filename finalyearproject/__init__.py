from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '5445bnb5g43nbj3fg34bn3443bm45543'
 # Connection String to connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://mydb3285oc:xi6gas@mysql1.it.nuigalway.ie/mydb3285"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from finalyearproject import routes