import os
from flask import Flask, g, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.http import HTTP_STATUS_CODES
import jwt

from seaoligo_common.config import config

db = SQLAlchemy()


def create_app(config_name):
    """
    Create a Flask application using the app factory pattern.

    :param config_name: Setup app configuration.
    :return: Flask app
    """
    if not os.environ.get('SECRET_KEY'):
        raise NameError('App secret key must be defined!')

    if not os.environ.get('JWT_ACCESS_TOKEN_KEY'):
        raise NameError('JWT access token key must be defined!')

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config.from_pyfile('settings.py', silent=True)

    db.init_app(app)

    @app.errorhandler(500)
    def internal_server_error(e):
        db.session.rollback()
        payload = dict(
            error=HTTP_STATUS_CODES.get(500),
            status='fail',
            message='Internal server error.',
        )
        response = jsonify(payload)
        response.status_code = 500
        return response

    @app.before_request
    def current_user():
        auth_header = request.headers.get('Authorization', '')
        g.auth_header = auth_header
        access_token = auth_header.replace('Bearer ', '')

        if access_token:
            try:
                payload = jwt.decode(access_token, os.environ.get('JWT_ACCESS_TOKEN_KEY'), algorithms=['HS256'])
                g.current_user = payload
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                g.current_user = None
        else:
            g.current_user = None

    @app.after_request
    def add_header(response):
        server_id = os.getcwd().replace('/', '')
        response.headers['Server-Id'] = server_id

        return response

    @app.route('/')
    def index():
        server_id = os.getcwd().replace('/', '')
        response = jsonify({'message': f'{server_id} service is up!'})

        return response

    return app
