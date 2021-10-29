from flask import Flask,request,Response,make_response,jsonify
from flask import json
from stockInfo import *
import logging
from flask_restx import Api,Resource,Namespace
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://stock:Stock+123@localhost/stock'
db = SQLAlchemy(app)
api = Api(app)

import Controller.stock_info  
api.add_namespace(Controller.stock_info.api)


if __name__ != '__main__':
    print('init')
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
