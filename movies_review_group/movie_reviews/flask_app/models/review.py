from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, review, movie
from flask import flash

class Review:
    db = "movies"

    def __init__(self, data):
        self.id = data['id']
        self.body = data['body']
        self.recommended = data['recommended']
        self.date_reviewed = data['date_reviewed']
        self.user_id = data['user_id']
        self.movie_id = data['movie_id']
        
        
    @classmethod
    def save_review(cls, data):
        query = """
                INSERT INTO reviews (body,recommended,date_reviewed,user_id,movie_id) 
                VALUES(%(body)s,%(recommended)s,%(date_reviewed)s,%(user_id)s,%(movie_id)s)
                """
        return connectToMySQL(cls.db).query_db(query, data)
    
    
    @classmethod
    def review_update(cls,data):
        query = """
            UPDATE reviews
            SET body = %(body)s, recommended = %(recommended)s, date_reviewed = %(date_reviewed)s, user_id = %(user_id)s, movie_id = %(movie_id)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)
    
    def get_movie_name(self):
        query = " SELECT title FROM movies WHERE id = %(movie_id)s;"
        data = {"movie_id": self.movie_id}
        result = connectToMySQL(self.db).query_db(query, data)
        return result[0]['title']
    
    def get_first_name(self):
        query = " SELECT first_name FROM users WHERE id = %(user_id)s;"
        data = {"user_id": self.user_id}
        result = connectToMySQL(self.db).query_db(query, data)
        return result[0]['first_name']
    
    @classmethod
    def get_all_reviews(cls):
        query = "SELECT * FROM reviews;"
        results = connectToMySQL(cls.db).query_db(query)

        all_reviews = []
        for one_review in results:
            all_reviews.append(cls(one_review))
        return all_reviews
    
    
    @classmethod
    def delete_review(cls, data):
        query = """
                DELETE FROM reviews WHERE id = %(id)s;
            """
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_one_review(cls, data):
        query = """
            SELECT * FROM reviews WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM reviews
                JOIN users on reviews.user_id = users.id
                WHERE reviews.id = %(id)s;
                """
        result = connectToMySQL("movies").query_db(query,data)
        if not result:
            return False

        result = result[0]
        this_review = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_review.user = user.User(user_data)
        return this_review
    
    @classmethod
    def get_all_reviews_with_users(cls):
        query = """
        SELECT * FROM reviews JOIN users ON reviews.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        review_object_list = []
        for each_review_dictionary in results:
            print(each_review_dictionary)
            new_review_object = cls(each_review_dictionary)
            new_user_dictionary = {
                "id": each_review_dictionary["users.id"],
                "first_name": each_review_dictionary["first_name"],
                "last_name": each_review_dictionary["last_name"],
                "email": each_review_dictionary["email"],
                "password": each_review_dictionary["password"],
                "created_at": each_review_dictionary["users.created_at"],
                "updated_at": each_review_dictionary["users.updated_at"],
            }
            new_user_object = user.User(new_user_dictionary)
            new_review_object.user = new_user_object
            review_object_list.append(new_review_object)
        return review_object_list
    
    
    @staticmethod
    def validate_review(review):
        is_valid = True

        if len(review['body']) < 5:
            flash("Review must be atleat 3 characters.", "review")
            is_valid = False

        if len(review['date_reviewed']) < 3:
            flash("Date cannot be left empty.", "review")
            is_valid = False
            
        if "recommended" not in review:
            flash(" Recommended cannot be left Empty")
            is_valid = False
        return is_valid