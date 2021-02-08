from flask import Flask,request,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse,parse_qs,parse_qsl

# initialise app
app=Flask(__name__)

# set up database
ENV='dev'
#ENV='heroku' -- when deployed in heroku

if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:sap@localhost/sap' # connect with local database
# elif ENV=='heroku':
#     app.debug=False
#     app.config[''] # connect with heroku database, need to be filled

# database module
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Short_url(db.Model):
    __tablename__='temp'
    id=db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String(120),unique=True)
    host=db.Column(db.String(120),unique=False)
    path=db.Column(db.String(120),unique=False)
    hash=db.Column(db.String(120),unique=False)
    
    def __init__(self,url,host,path,hash):
        self.url=url
        self.host=host
        self.path=path
        self.hash=hash

# homepage: get users input URL (note: this is part is necessary only when want to visualise the input in a webpage.
# If directly processing users' input from request url then this part is useless) 
@app.route("/")
def index():
    return 

# processing users' input, generate MD5 hash and write in db
@app.route("/submit")
def submit():

    # @xinyao, please let us keep things aligned:
    # 1. logic of generating hash: extract the host (i.e. domain name), path from input url, can reference
    # functions in urllib package
    # then convert the path into hash.
    # 2. input variables' names aligned: url, host, path, hash

    # parse url and generate hash


    # write into database
    data=Short_url(url,host,path,hash)
    print(type(data))
    db.session.add(data)
    db.session.commit()

    return # can return a success page or simply a message

# identify users shorten url input and redirect
@app.route("/access/<path:short_url>")
def access(short_url):
    str_short_url=str(short_url)
    hash_code=str_short_url.split("/")[1]
    for instance in db.session.query(Short_url).filter(Short_url.hash==hash_code):
       return redirect(instance.url) # redirection

# entrance
if __name__=='__main__':
    app.run()