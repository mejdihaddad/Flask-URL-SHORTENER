from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random
import urllib.request
import urllib.error
import urllib.error
import os
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
path = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)
class UrlShortener(db.Model):
    __tablename__ = 'shortener'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.Text)
    shortUrl = db.Column(db.Text)
    def __init__(self, url, shortUrl):
        self.url = url
        self.shortUrl = shortUrl
    def __repr__(self):
        return "Url : {} and ShortUrl is : {}".format(self.url, self.shortUrl)
def validate(url):
    try:
        urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError as e:
        print('HTTPError:',e.code,url)
    except urllib.error.URLError as e:
        print('URLErroe:',e.reason,url)
    except Exception as e:
        print('Exception',str(e),url)
    return False

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":  
      url = request.form.get("url")
      short=''
      ch="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" 
      if validate(url):
       for i in range(15):
         short+= random.choice(ch)
       info=UrlShortener(url=url,shortUrl=short)
       db.session.add(info)
       db.session.commit()
      else :
        print("Please Enter Valid URL ")
      return render_template("home.html", urls=short)
    return render_template("home.html")

@app.route('/history',methods=["GET","POST"])
def history():
    histoUrls=UrlShortener.query.all()
    return render_template("history.html",histo=histoUrls)

if __name__ == '__main__':
    app.run(debug=True)