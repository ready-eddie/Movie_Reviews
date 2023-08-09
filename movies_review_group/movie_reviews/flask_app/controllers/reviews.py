from flask import render_template, redirect, session, request
from flask_app import app

from flask_app.models import user, review, movie


# Visible routes


@app.route("/comments")
def all_posted_reviews_page():
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'id' : session['user_id']
    }
    return render_template("posted_reviews.html", user_logged = user.User.get_user_by_id(data), all_reviews = review.Review.get_all_reviews_with_users())


@app.route("/new/review")
def add_review_page():
    if 'user_id' not in session:
        return redirect("/")
    data = {
        'id': session['user_id']
    }
    all_movies = movie.Movie.get_all_movies()
    return render_template("new_review.html", user_logged=user.User.get_user_by_id(data), all_movies=all_movies)


@app.route("/reviews/add_to_db", methods=["POST"])
def add_review_to_db():
    if 'user_id' not in session:
        return redirect('/')
    if not review.Review.validate_review(request.form):
        return redirect('/new/review')
    
    data = {
        'user_id': session['user_id'],
        'movie_id': request.form['movie_id'],
        'body': request.form['body'],
        'recommended': request.form['recommended'],
        'date_reviewed': request.form['date_reviewed'],
    }
    review.Review.save_review(data)
    return redirect('/comments')


@app.route("/edit/<int:id>")
def edit_review_page(id):
    one_review = review.Review.get_one_review({"id": id})
    all_movies = movie.Movie.get_all_movies()
    return render_template("edit_review.html", one_review = one_review, all_movies=all_movies)


@app.route("/edit/reviews/", methods=["POST"])
def update_review():
    if not review.Review.validate_review(request.form):
        return redirect(request.referrer)
    else:
        data = {
            'body': request.form['body'],
            'recommended': request.form['recommended'],
            'date_reviewed': request.form['date_reviewed'],
            'user_id': session['user_id'],
            'movie_id': request.form['movie_id'],
            'id': request.form['id']
        }
        review.Review.review_update(data)
        return redirect('/comments')


@app.route('/delete/review/<int:id>')
def delete_review(id):
    data = {
        'id': id
    }
    review.Review.delete_review(data)
    return redirect(request.referrer)


@app.route("/show/<int:id>")
def review_info_page(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id,
    }
    form_data = {
        'id': session['user_id']
    }
    one_review = review.Review.get_one_review(data)
    return render_template("show_review.html", one_review=one_review,user_logged=user.User.get_user_by_id(form_data))





