from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Join_ride:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.ride_id = data['ride_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #CREATE A Join Ride
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO join_rides (user_id, ride_id)
            VALUES (%(user_id)s, %(ride_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    #! GET ALL THE RIDES ID'S JOINED BY ONE USER
    @classmethod
    def get_rides_id_for_user(cls, data):
        joined_rides_id = []
        query = """SELECT rides.id FROM rides 
        JOIN join_rides 
        ON join_rides.ride_id = rides.id
        JOIN users
        ON  users.id = join_rides.user_id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results :
            for row in results:
                joined_rides_id.append(row['id'])
        return joined_rides_id

    #DELETE ALL THE TRIPS FOR DELETED RIDE (By Driver)
    @classmethod
    def deleteByRide(cls, data):
        query = "DELETE FROM join_rides WHERE ride_id = %(ride_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    #CANCEL A TRIP (By The Passenger)
    @classmethod
    def cancel(cls, data):
        query = "DELETE FROM join_rides WHERE user_id = %(user_id)s AND ride_id = %(ride_id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
