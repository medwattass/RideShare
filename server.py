from flask_app import app
from flask_cors import CORS
from flask_app.controllers import users, rides, join_rides, rates, comments, messages
from flask import request, render_template

CORS(app)

# CATCH ANY UNDEFINED ROUTE
@app.errorhandler(404)
def page_not_found(error):
    route = request.path
    return render_template('404.html', route = route)


if __name__ == "__main__":
    app.run(debug=True)