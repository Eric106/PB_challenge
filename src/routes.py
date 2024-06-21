from flask import request, jsonify
from decimal import Decimal
from functools import wraps
from . import app
from .modules.model import User, Investment
from .modules.auth import Auth_Service
from .modules.config import CONFIG


AUTH = Auth_Service()
app.secret_key = CONFIG.secret_key

def auth_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        has_access = AUTH.verify_token(request.headers)
        if not has_access:
            return jsonify({'message': 'Unauthorized'}), 401
        return func(*args, **kwargs)
    return decorated

@app.route("/", methods=['POST','GET'])
def root():
    return jsonify({'success': True, 'message':'hola mundo'}), 200

@app.route("/create_user", methods=['POST'])
def create_user():
    try:
        user = User(
            user_name=request.json['user_name'],
            password=request.json['password']
        )
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    user.create()
    if user.is_valid:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401
    
@app.route("/delete_user", methods=['DELETE'])
@auth_required
def delete_user():
    try:
        jwt_payload = AUTH.get_payload(request.headers)
        user = User(user_id=jwt_payload['user_id'])
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    
    user.delete()
    if user.is_valid:
        return jsonify({'success': True}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route("/login", methods=['POST'])
def login():
    try:
        user = User(
            user_name=request.json['user_name'],
            password=request.json['password']
        )
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    user.verify_login()
    if user.is_valid:
        return jsonify({'success': True,
                        "token": AUTH.get_token(user)}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401

@app.route("/create_investment", methods=['POST'])
@auth_required
def create_investment():
    try:
        investment = Investment()
        investment.from_dict(request.json)
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    
    investment.create()
    if investment.is_null():
        return jsonify({'message': 'Forbidden'}), 403

    return jsonify({'success': True,
                    'investment':investment.to_dict()}), 200

@app.route("/calc_investment", methods=['POST'])
@auth_required
def calc_investment():
    try:
        jwt_payload = AUTH.get_payload(request.headers)
        investment = Investment(
            user_id=jwt_payload['user_id'],
            total_investment=Decimal(request.json['total_investment']),
            pb_points=Decimal(request.json['pb_points']),
            pay_method=request.json['pay_method'],
        )
    except (KeyError,TypeError):
        return jsonify({'message': 'Bad Request'}), 400
    
    return jsonify({'success': True,
                    'investment':investment.to_dict()}), 200

@app.route("/get_investment", methods=['GET'])
@auth_required
def get_investment():
    try:
        jwt_payload = AUTH.get_payload(request.headers)
        investment = Investment(
            investment_id=request.json['investment_id'],
            user_id=jwt_payload['user_id']
        )
        investment.get()
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    
    if investment.is_null():
        return jsonify({'message': 'Not Found'}), 404

    return jsonify({'success': True,
                    'investment':investment.to_dict()}), 200

@app.route("/get_investments", methods=['GET'])
@auth_required
def get_investments():
    try:
        jwt_payload = AUTH.get_payload(request.headers)
        user = User(
            user_id=jwt_payload['user_id']
        )
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    investments = user.get_investments()
    return jsonify({'success': True,
                    'investments':investments}), 200

@app.route("/update_investment", methods=['POST'])
@auth_required
def update_investment():
    try:
        jwt_payload = AUTH.get_payload(request.headers)
        investment = Investment(
            investment_id=request.json['investment_id'],
            user_id=jwt_payload['user_id']
        )
        investment.get()
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    
    if investment.is_null():
        return jsonify({'message': 'Not Found'}), 404
    
    investment.update(request.json)

    return jsonify({'success': True,
                    'investment': investment.to_dict()}), 200

@app.route("/delete_investment", methods=['DELETE'])
@auth_required
def delete_investment():
    try:
        jwt_payload = AUTH.get_payload(request.headers)
        investment = Investment(
            investment_id=request.json['investment_id'],
            user_id=jwt_payload['user_id']
        )
        investment.get()
    except KeyError:
        return jsonify({'message': 'Bad Request'}), 400
    
    if investment.is_null():
        return jsonify({'message': 'Not Found'}), 404

    investment.delete()

    return jsonify({'success': True,
                    'investment': investment.to_dict()}), 200
