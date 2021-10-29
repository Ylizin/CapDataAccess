from flask_restx import Api,Resource,Namespace
from flask import Flask,request,Response,make_response,jsonify
from stockInfo import *

# it will add a blueprint with path 'stock'
api = Namespace('stock',description='apis for prices.')
# support nest attribute 
@api.route('/info/<stock_code>')
@api.doc(params={'stock_code':{'description':'The code of a sotck','in':'path'}})
class Info(Resource):
    @api.response(200,'get prices')
    @api.response(4010,'invalid code')
    def get(self,stock_code):
        s = Stock(stock_code)
        data = s.get_df()
        return jsonify(data['close'].tolist())