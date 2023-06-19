from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Rate:
    def __init__(self , data ):
        self.id = data['id']
        self.profile_id = data['profile_id']
        self.rater_id = data['rater_id']
        self.rate = data['rate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO rates (profile_id, rater_id, rate) VALUES (%(profile_id)s, %(rater_id)s, %(rate)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_profile_raters_id(cls, data):
        query = """
            SELECT rater_id FROM rates 
            WHERE profile_id = %(profile_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_rater_profile_rate(cls, data):
        query = """
            SELECT rate FROM rates 
            WHERE rater_id = %(rater_id)s AND profile_id = %(profile_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def updaterate(cls, data):
        query = """
            UPDATE rates SET 
            rate = %(rate)s
            WHERE rater_id = %(rater_id)s AND profile_id = %(profile_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def getAvgRate(cls, data):
        query = "SELECT AVG(rate) AS rate FROM rates where profile_id =  %(id)s;"
        rate = connectToMySQL(DATABASE).query_db(query, data)
        if rate[0]['rate'] == None:
            return 'N/A'
        return round(rate[0]['rate'], 2)

