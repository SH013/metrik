from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from wtf import RegistrationForm
from database import Users, corre, CopyBase


app = Flask(__name__)
app.config["SECRET_KEY"] = '79537d00f4834892986f09a100aa1edf'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Azritmix1234@localhost:5432/datadb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@app.route("/")
def index():
    info = []
    try:
        info = Users.query.all()
    except:
        print("Ошибка чтения из БД")

    return render_template("index.html", title="Главная", list=info)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                u = Users(date=form.date.data, value=form.value.data,p_date=form.p_date.data,p_value=form.p_value.data)
                db.session.add(u)
                db.session.commit()
                CopyBase()
        except:
                db.session.rollback()
                print("Ошибка добавления в БД")

        return redirect(url_for('index'))

    return render_template("register.html", title="Регистрация", form = form)

@app.route("/result" )
def result():    
    info = []
    try:        
        info = corre.query.all()
    except:
        print("Ошибка чтения из БД")

    return render_template("result.html", title="Главная", list=info)


if __name__ == "__main__":
    app.run(debug=True)