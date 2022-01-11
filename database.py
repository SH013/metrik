import pandas as pd
import psycopg2
from config import host, user, password, db_name
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Azritmix1234@localhost:5432/datadb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    p_value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    p_date = db.Column(db.DateTime, nullable=False)
    

    def __init__(self, p_value, value, date, p_date):
        self.value = value
        self.p_value = p_value
        self.date = date
        self.p_date = p_date

    def __repr__(self):
         return f"<users {self.id}>"
    
class corre(db.Model):
    __tablename__ = 'correlation'

    id = db.Column(db.Integer, primary_key=True)
    curr = db.Column(db.String) 


    def __init__(self, curr):
        self.curr = curr
    
    def __repr__(self):
         return f"<users {self.id}>"


def CopyBase():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
    connection.autocommit = True

    try:
        with connection.cursor() as cursor:
            cursor.execute(
            """copy (Select * From users) To 'C:/metrik/table.csv' With CSV DELIMITER ',' HEADER;"""
                )
            connection.commit()
            print("[INFO] Table copy ")

            tab = pd.read_csv('table.csv')
            tab.set_index('id', inplace = True)
            gr=tab.groupby(['p_date', 'date']).corr()
            print (gr)
        with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO correlation (curr) VALUES
                    ( %s);""", (  f'{gr}',  )
                )
                print("[INFO] Table inserted successfully")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")

