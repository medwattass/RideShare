from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import user

class Ride:
    def __init__(self , data ):
        self.id = data['id']
        self.user_id = data['user_id']
        self.from_location = data['from_location']
        self.to_location = data['to_location']
        self.when_time = data['when_time']
        self.seats = data['seats']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @staticmethod
    def validate(data):
        errorMessages = []
        if len(data['from_location'])<2:
            errorMessages.append("From Location Must Be At Least 2 Characters")

        if len(data['to_location'])<2:
            errorMessages.append("Destination Must Be At Least 2 Characters")
        
        if data['when_time']=="":
            errorMessages.append("Ride Must Have A Date and Time")
        try:
            if len(data['seats'])<1 or int(data['seats'])<0:
                errorMessages.append("Ride Must Have A Number Of Seats")
        except:
            return errorMessages
        return errorMessages

    @classmethod
    def save(cls, data):
        query = "INSERT INTO rides (user_id, from_location, to_location, when_time, seats) VALUES (%(user_id)s, %(from_location)s, %(to_location)s, %(when_time)s, %(seats)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
            SELECT * FROM rides JOIN users ON rides.user_id = users.id.
        """
        results = connectToMySQL(DATABASE).query_db(query)
        rides =[]
        if results:
            for row in results:
                ride = cls(row)
                ride.driver = {'id' : row['user_id'],
                                'first_name' : row['first_name'],
                                'last_name' : row['last_name'],
                                'email' : row['email']
                            }
                rides.append(ride)
        else:
            rides = 'No Rides Yet'
        return rides
    
    # - GET ONE BY ID
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM rides WHERE id = %(id)s; 
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def get_created_rides(cls, data):
        query = """
            SELECT * FROM rides JOIN users ON rides.user_id = users.id WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        created_rides = []
        for row_from_db in results:
            ride_data = {
                "id" : row_from_db["id"],
                "user_id" : row_from_db["users.id"],
                "from_location" : row_from_db["from_location"],
                "to_location" : row_from_db["to_location"],
                "when_time" : row_from_db["when_time"],
                "seats" : row_from_db["seats"],
                "created_at" : row_from_db["created_at"],
                "updated_at" : row_from_db["updated_at"]
            }
            created_rides.append(ride_data)
        return created_rides

    @classmethod
    def get_created_rides_id(cls, data):
        created_rides_id = []
        query = """
            SELECT id FROM rides WHERE user_id = %(user_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        for row in results:
            created_rides_id.append(row['id'])
        return created_rides_id

    @classmethod
    def update(cls, data):
        query = """
            UPDATE rides SET 
            user_id = %(user_id)s, from_location = %(from_location)s, to_location = %(to_location)s, when_time = %(when_time)s, seats = %(seats)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def updateSeats(cls, data):
        query = """
            UPDATE rides SET 
            seats = seats - 1
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def addSeat(cls, data):
        query = """
            UPDATE rides SET 
            seats = seats + 1
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_passengers(cls, data):
        query = """SELECT * FROM rides 
        JOIN join_rides ON join_rides.ride_id = rides.id 
        LEFT JOIN users ON join_rides.user_id = users.id 
        WHERE rides.id = %(id)s ORDER BY users.first_name;"""
        results = connectToMySQL(DATABASE).query_db(query , data)
        passengers = []
        if (len(results)>0):
            for row_from_db in results:
                user_data = {
                    "id" : row_from_db["users.id"],
                    "ride_id" : row_from_db["ride_id"],
                    "first_name" : row_from_db["first_name"],
                    "last_name" : row_from_db["last_name"],
                    "email" : row_from_db["email"],
                    "password" : row_from_db["password"],
                    "created_at" : row_from_db["users.created_at"],
                    "updated_at" : row_from_db["users.updated_at"]
                }
                passengers.append(user.User(user_data))
        return passengers
    
    #Add user to the list that took the ride
    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO join_rides (ride_id, user_id) VALUES (%(ride_id)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM rides WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #FIND RIDES
    @classmethod
    def findRides(cls, data):
        query = """SELECT * FROM rides 
            JOIN users ON rides.user_id = users.id 
            WHERE rides.from_location LIKE %(from_location)s 
            AND rides.to_location LIKE %(to_location)s
            AND rides.when_time BETWEEN (%(when_time)s - INTERVAL '12' HOUR) AND (%(when_time)s + INTERVAL '12' HOUR)
            AND rides.seats >0 
            AND rides.when_time >= NOW();
            """
        results = connectToMySQL(DATABASE).query_db(query, data)
        rides = []
        if results:
            for row in results:
                ride = {
                    'id' : row['id'],
                    'user_id' : row['user_id'],
                    'from_location' : row['from_location'],
                    'to_location' : row['to_location'],
                    'when_time' : row['when_time'],
                    'seats' : row['seats'],
                    'driver' : f"{row['first_name']} {row['last_name']}",
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }
                rides.append(ride)
        return rides


    #!SEARCH ride BY FILTER (TITLE, AUTHOR, DESCRIPTION)
    @classmethod
    def search(cls, data):
        query = """SELECT * FROM rides 
            JOIN users ON users.id = rides.user_id 
            WHERE {filter} LIKE %(search)s 
            AND rides.when_time >= NOW();
            """
        results = connectToMySQL(DATABASE).query_db(query.format(filter=data['filter']), data)
        rides = []
        if results:
            for row in results:
                ride = cls(row)
                ride.driver = {'id' : row['user_id'],
                                    'first_name' : row['first_name'],
                                    'last_name' : row['last_name'],
                                    'email' : row['email']
                                }
                rides.append(ride)
        return rides
    
    # ?SEARCH ride BY DRIVER
    @classmethod
    def searchByDriver(cls, data):
        query = """SELECT * FROM rides 
            JOIN users ON rides.user_id = users.id 
            WHERE (users.first_name LIKE %(search)s 
            OR users.last_name LIKE %(search)s)
            AND rides.when_time >= NOW();
            """
        results = connectToMySQL(DATABASE).query_db(query, data)
        rides = []
        if results:
            for row in results:
                ride = cls(row)
                ride.driver = {'id' : row['users.id'],
                                    'first_name' : row['first_name'],
                                    'last_name' : row['last_name'],
                                    'email' : row['email']
                                }
                rides.append(ride)
        return rides
    
    
    @classmethod
    def countCreatedRidesForUser(cls, data):
        query = "SELECT Count(*) AS numbRides FROM rides WHERE user_id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result[0]['numbRides']>0 :
            return result[0]['numbRides']
        return 0
