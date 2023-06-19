from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Message:
    def __init__(self, data):
        self.id = data['id']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.message = data['message']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(data):
        if len(data['message'])<2:
            return False
        return True
    
    @classmethod
    def send(cls, data):
        query = """
            INSERT INTO messages (sender_id, receiver_id, message, ride_id)
            VALUES (%(sender_id)s, %(receiver_id)s, %(message)s, %(ride_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def remove_message(cls, data):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def asReadMessage(cls, data):
        query = """
            UPDATE messages SET 
            status = 1
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def showAllMessagesForUser(cls, data):
        query = """SELECT * FROM users 
        JOIN messages ON messages.sender_id = users.id
        JOIN rides ON messages.ride_id = rides.id
        WHERE receiver_id = %(id)s;"""
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def showActifMessagesForUser(cls, data):
        query = """SELECT * FROM users 
        LEFT JOIN messages ON messages.sender_id = users.id
        LEFT JOIN rides ON messages.ride_id = rides.id
        WHERE receiver_id = %(id)s AND status = 0 ORDER BY messages.created_at DESC;"""
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def countActifMessagesForUser(cls, data):
        query = "SELECT Count(*) AS numbMessages FROM messages WHERE receiver_id = %(id)s AND status = 0;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if result[0]['numbMessages']>0 :
            return result[0]['numbMessages']
        return 0