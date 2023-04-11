import os
from functools import wraps
from flask import Flask, render_template, Response, current_app, request, jsonify
from .models import db, UserHome, Boards
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt, verify_jwt_in_request, jwt_required

# import urllib.request, json
# from flask_mqtt import Mqtt
# from flask_caching import Cache


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config["SECRET_KEY"] = 'dev'
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://home:admin@localhost:5432/home_db"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = "super-secret"
    jwt = JWTManager(app)

    # Creating a custom decorator @admin_required to check user.role in the jwt access token as additional claims
    def admin_required():
        def wrapper(fn):
            @wraps(fn)
            def decorator(*args, **kwargs):
                verify_jwt_in_request()
                claims = get_jwt()
                if claims["is_administrator"]:
                    return fn(*args, **kwargs)
                else:
                    return 'admin only', 403

            return decorator

        return wrapper

    """

    app.config['MQTT_BROKER_URL'] = 'localhost'
    app.config['MQTT_BROKER_PORT'] = 1883
    app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds
    app.config['MQTT_TLS_ENABLED'] = False  # If your server supports TLS, set it True
    mqtt_client = Mqtt(app)

    cache = Cache(app)

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected successfully')
            mqtt_client.subscribe('t')
            mqtt_client.subscribe('h') 
        else:
            print('Bad connection. Code:', rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        data = {
            'topic' : message.topic,
            'payload' : message.payload.decode('utf-8')
        }
        if message.topic == 't':
            cache.set("room_temp", message.payload.decode('utf-8'))
        
        if message.topic == 'h':
            cache.set("room_humidity", message.payload.decode('utf-8'))

        print('Received message on topic: {topic} with payload: {payload}'.format(**data))
     """

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import api
    app.register_blueprint(api.bp)

    
    @app.route('/')
    @admin_required()
    def index():
        return 'Hello, World!'
    
    @app.route('/test')
    @jwt_required
    @admin_required()
    def test():
        return "hello"

    @app.route('/query')
    def query():
        users = UserHome.query.all()
        boards = Boards.query.all()
        return render_template('db.html', boards=boards, users=users)

    return app
