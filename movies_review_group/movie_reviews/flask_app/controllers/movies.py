from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models import user, review, movie


@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id': session['user_id']
    }
    all_movies = movie.Movie.get_all_movies()
    return render_template("dashboard.html", all_movies=all_movies)
