from flask_app.models import user
from flask import flash
from flask import render_template, redirect, session, request
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/")
def home_page():
    return render_template("login_reg.html")


@app.route("/register", methods=["POST"])
def register_new_user():
    if not user.User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = user.User.save(data)
    session['user_id'] = id
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login_user():
    data = {
        "email": request.form["email"]
    }
    found_user = user.User.get_by_email(data)

    if not found_user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(found_user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = found_user.id
    session['name'] = found_user.first_name
    return redirect('/dashboard')


@app.route("/logout")
def logout_user():
    session.clear()
    return redirect('/')
