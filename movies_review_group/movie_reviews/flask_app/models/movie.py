from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, review
from flask import flash


class Movie:
    db = "movies"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        
        self.reviews = []

    @classmethod
    def save_movie(cls, data):
        query = " INSERT INTO movies (title) VALUES (%(title)s);"
        return connectToMySQL(cls.db).query_db(query, data)
    
    
    @classmethod
    def get_all_movies(cls):
        query = """
            SELECT * FROM movies;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_movies = []
        for one_movie in results:
            all_movies.append(cls(one_movie))
        return all_movies

    @classmethod
    def get_one_movie(cls, data):
        query = """
            SELECT * FROM movies
            WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def update_movie(cls, data):
        query = """
            UPDATE movies
            SET title = %(title)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_movie(cls, data):
        query = """
            DELETE FROM movies WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_movie(movie):
        is_valid = True

        if len(movie['title']) < 3:
            flash("movie title must not be blank.")
            is_valid = False

        return is_valid


    @classmethod
    def get_movie_with_review(cls, data):
        query = """
            SELECT * FROM movies 
            JOIN reviews ON movies.id = reviews.movie_id
            WHERE movies.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        one_movie = cls(results[0])
        
        for review_dict in results:
            review_dict = {
                "id": review_dict["reviews.id"],
                "body": review_dict["body"],
                "recommended": review_dict["recommended"],
                "date_reviewed": review_dict["date_reviewed"],
                "user_id": review_dict["user_id"],
                "movie_id": review_dict["movie_id"]
            }
            one_review = review.Review(review_dict)
            one_movie.reviews.append(one_review)
        return one_movie
        
    # @classmethod
    # def get_by_id(cls,data):
    #     query = """
    #             SELECT * FROM movies
    #             JOIN users on movies.user_id = users.id
    #             WHERE movies.id = %(id)s;
    #             """
    #     result = connectToMySQL("movies").query_db(query,data)
    #     if not result:
    #         return False

    #     result = result[0]
    #     this_movie = cls(result)
    #     user_data = {
    #             "id": result['users.id'],
    #             "first_name": result['first_name'],
    #             "last_name": result['last_name'],
    #             "email": result['email'],
    #             "password": "",
    #             "created_at": result['users.created_at'],
    #             "updated_at": result['users.updated_at']
    #     }
    #     this_movie.user = user.User(user_data)
    #     return this_movie
        