from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import ride
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.joined_rides = []
    
    # =====================Validations=====================
    #? PASSWORD MUST HAVE AT LEAST ONE UPPERCASE AND ONE NUMBER
    
    @staticmethod
    def verify_password(str):
        upper_in = False
        number_in = False
        
        for char in str:
            if char.isupper():
                upper_in = True
            if char.isdigit():
                number_in = True
        
        if upper_in and number_in:
            return True
        else:
            return False

    @staticmethod
    def validate(data):
        errorMessages = []
        if len(data['first_name'])<2:
            errorMessages.append("First Name must contain at least 2 characters")

        if len(data['last_name'])<2:
            errorMessages.append("Last Name must contain at least 2 characters")
            
        if not EMAIL_REGEX.match(data['email']): 
            errorMessages.append("Email not valid")
        elif User.get_by_email({'email':data['email']}):
            errorMessages.append("Email Already Exists")

        if len(data['password']) <8:
            errorMessages.append("Password Must Have More Than 8 Characters")
        elif not User.verify_password(data['password']) :
            errorMessages.append("Password Must Contain At Least A Number And An Uppercase Character")
        elif data['password']!= data['confirm_password']:
            errorMessages.append("Password and Confirmation Doesn't Match")
        return errorMessages

    # =======================Queries=======================

    # - CREATE
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # - GET ONE BY EMAIL
    @classmethod
    def get_by_email(cls,data):
        query = """
            SELECT * FROM users WHERE email = %(email)s; 
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    # - GET ONE BY ID
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM users WHERE id = %(id)s; 
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])


    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL(DATABASE).query_db(query)
    
    @classmethod
    def get_user_with_rides(cls, data):
        #fixed this query by changing the book_id to ride_id
        query = "SELECT * FROM users LEFT JOIN join_rides ON join_rides.user_id = users.id LEFT JOIN rides ON join_rides.ride_id = rides.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query , data)
        user = cls(results[0])
        for row_from_db in results:
            if row_from_db["rides.id"]:
                book_data = {
                    "id" : row_from_db["rides.id"],
                    "user_id" : row_from_db['user_id'],
                    "from_location" : row_from_db['from_location'],
                    "to_location" : row_from_db['to_location'],
                    "when_time" : row_from_db['when_time'],
                    "seats" : row_from_db['seats'],
                    "created_at" : row_from_db["rides.created_at"],
                    "updated_at" : row_from_db["rides.updated_at"]
                }
                user.joined_rides.append(ride.Ride(book_data))
        return user
    
    #Add user's Joined Ride to join_rides table
    @classmethod
    def add_ride(cls, data):
        query = "INSERT INTO likes (ride_id, user_id) VALUES (%(ride_id)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)