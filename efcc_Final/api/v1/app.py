#!/usr/bin/python3
"""A flask application that runs the endpoints"""
from flask import Flask, render_template, make_response, jsonify
from os import getenv
from dotenv import load_dotenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
load_dotenv()
app.config["SECRET_KEY"] = getenv('APP_SECRET_KEY')

@app.teardown_appcontext
def close_db(error):
    """Closes the data"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Custom error message"""
    response = jsonify({'error': 'Not Found'})
    return make_response(response)


if __name__ == "__main__":
    """Module runner"""
    # host = getenv("EFCC_MYSQL_HOST")
    # port = getenv("EFCC_MYSQL_PORT")
    # if not host:
    #     host = '0.0.0.0'
    # if not port:
    #     port = '5000'
    # app.run(host=host, port=port, threaded=True, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
