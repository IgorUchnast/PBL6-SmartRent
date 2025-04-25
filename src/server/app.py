from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
CORS(app)

jwt = JWTManager(app)

db = SQLAlchemy(app)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables dropped and created successfully.")
    app.run(host='0.0.0.0', port=8000, debug=True)
