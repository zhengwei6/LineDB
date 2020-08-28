from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

username = 'pixiu'
password = 'pixiu168!^*'
host = 'pixiu-dev.cqifhpvbr5zx.us-east-2.rds.amazonaws.com'
port = '3306'
database = 'db_line'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def delete_object(db_object):
  db.session.delete(db_object)
  db.session.commit()
  
def create_table():
  db.create_all()
  db.session.commit()

def update_database():
  db.session.commit()

