from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.poster_id = data['poster_id']
        self.profile_id = data['profile_id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate(data):
        if len(data['comment'])<2:
            return False
        return True
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO comments (profile_id, poster_id, comment)
            VALUES (%(profile_id)s, %(poster_id)s, %(comment)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM comments WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @classmethod
    def getAllByProfile(cls, data):
        query = """
            SELECT * FROM users
            JOIN comments ON users.id = comments.poster_id 
            WHERE comments.profile_id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def edit(cls, data):
        query = """UPDATE comments 
            SET comment = %(comment)s 
            WHERE id = %(id)s;
            """
        return connectToMySQL(DATABASE).query_db(query, data)