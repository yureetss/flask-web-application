from flask import Flask, render_template
from extensions import db
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

from app.authentification.authentification import authentification
from app.registration.registration import registration
from app.records.records import records
from app.account.account import user_account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db.init_app(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.register_blueprint(authentification)
app.register_blueprint(registration)
app.register_blueprint(records)
app.register_blueprint(user_account, url_prefix='/account')

app.config['UPLOAD_FOLDER'] = 'static/uploads/avatars'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_404.html'), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    # app.run(host='0.0.0.0')