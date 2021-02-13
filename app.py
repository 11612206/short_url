from flask import Flask,request,render_template,redirect
from wtforms import Form, FloatField
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse,parse_qs,parse_qsl
import hashlib

# initialise app
app=Flask(__name__)

#create md5 object
md5 = hashlib.md5()

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
#Xinjie, here I use wtforms instead of request. I can change if you want or some error occurs during next step
@app.route("/submit", method='POST')
def submit():
    
    #get url
    url = request.form.get("url")
    url = urlparse(url)
    host = url.netloc
    path = url.path
    hash = get_md5(path)
    new_url= host + '/'+ hash

    # write into database
    data=Short_url(url,host,path,hash)
    print(type(data))
    db.session.add(data)
    db.session.commit()

    return render_template("submit.html", s=new_url)

# @Xinjie, one problem here is that md5 hash generate 128-bit hash output(16 digits), not the same as the example from Justin
# the 6 digit shorten form cannot be achieved using hash, normally we need to design our own transformation method
# I will drop him an email to discuss about this

#MD5 hash
def get_md5(path):
    md5.update(path.encode(encoding='utf-8'))
    return md5.hexdigest()


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
