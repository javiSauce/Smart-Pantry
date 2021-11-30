# import psycopg2
from flask import Flask, request, render_template, url_for, flash, session, redirect
# from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from random import randint
from config import Config
# from flask_migrate import Migrate
# from models import Ingredient, Admin, Chef, RegularUser

# conn = psycopg2.connect(database="fsing047", user="fsing047", password="Lallouz24",host="web0.site.uottawa.ca", port="15432")
# cursor = conn.cursor()


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4321@127.0.0.1:5432/smartpantry'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = Config.SECRET_KEY
db = SQLAlchemy(app)
# sess=Session()
# migrate = Migrate(app,db)

print(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'user':#app.config['user']:
            error = 'Invalid username'
        elif request.form['password'] != 'pass':#app.config['pass']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/pickUser')
def pickUser():
    return render_template('pickUser.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/chef')
def chef():
    return render_template('chef.html')

@app.route('/userIngredientList')
def show_entries():

    cur = db.engine.execute('select * from smartpantry.ingredient where count>=1 order by ingr_id desc')
    entries = cur.fetchall()
    return render_template('userIngredientList.html', entries=entries)

@app.route('/userAddIngredients', methods=['POST'])
def add_entry():
    sql="insert into smartpantry.ingredient (ingr_id,name, count,price_per_item,threshold) values ("+str(randint(10000,999999))+",'"+request.form['name']+"',"+request.form['count']+","+request.form['price']+","+request.form['threshold']+")"
    db.engine.execute(sql)
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/userRemoveIngredients', methods=['POST'])
def remove_entry():
    sql="delete from smartpantry.ingredient where ingr_id="+str(request.form['ingr_id'])
    db.engine.execute(sql)
    flash('New entry was successfully deleted')
    return redirect(url_for('show_entries'))


# @app.route('/post_ingredient')# methods=['POST'])
# def post_ingredient():
#     ingr = None
#     if request.method == 'POST':
#         ingr = Ingredient(request.form['Ingredient'], request.form['Quantity'])
#         db.session.add(ingr)
#         db.session.commit()
#         return render_template('userIngredientList.html')
#     return render_template('userIngredientList.html')

# @app.route('/all_ingredient', methods=['GET','POST'])
# def all_ingredient():
#     ing = Ingredient.query.filter_by(ingredient=ingredient).first()
#     ingr = db.session.query(Ingredient).all()
#     return render_template('userIngredientList.html', ingr=ingr,ing=ing)


if __name__ == "__main__":
    # sess.init_app
    app.debug = True
    app.run()
