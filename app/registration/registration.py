from flask import Blueprint, render_template, request, redirect, session, current_app
from extensions import db
from models import Person
import re
from werkzeug.utils import secure_filename
import uuid
import os

registration = Blueprint('registration', __name__, template_folder = 'templates')

USERNAME_REGEX = r'^[A-Za-z0-9_]{5,20}$'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,64}$'
EMAIL_REGEX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,10}$'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def user_exists(username):
    user = Person.query.filter_by(username=username).first()
    return user is not None

def mail_exists(mail):
    mail = Person.query.filter_by(mail=mail).first()
    return mail is not None

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@registration.route('/signup', methods=['POST', 'GET'])
def signup():
    if 'user' in session:
        return render_template('index.html')
    
    if request.method == 'POST':
        mail = request.form['mail']
        username = request.form['username']
        password = request.form['password']
        file = request.files.get('avatar')

        if not re.fullmatch(USERNAME_REGEX, username):
            return render_template(
                'registration/signup.html',
                error_username_re="Имя пользователя должно быть от 5 до 20 символов и состоять только из букв, цифр или _."
            )
        
        if not re.fullmatch(EMAIL_REGEX, mail):
            return render_template(
                'registration/signup.html',
                error_email_re="Введите корректный e-mail в формате name@example.com."
            )
        
        
        if not re.fullmatch(PASSWORD_REGEX, password):
            return render_template(
                'registration/signup.html',
                error_password_re="Пароль должен быть длиной от 8 символов, содержать строчные, заглавные буквы, цифры и спецсимволы."
            )
            
        if not username or not password or not mail:
            error = "Пожалуйста, заполните все поля."
            return render_template('registration/signup.html', error=error)
        
        if user_exists(username):
            error_username=f"Пользователь с именем '{username}' уже существует."
            return render_template('registration/signup.html', error_username=error_username)
        
        if mail_exists(mail):
            error_mail=f"Пользователь с таким email уже существует."
            return render_template('registration/signup.html', error_mail=error_mail)
            

        person = Person(mail=mail, username=username)
        person.set_password(password)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_name = f"{uuid.uuid4()}.{ext}"

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name))

            person.avatar = unique_name

        try:
            db.session.add(person)
            db.session.commit()
            session['user'] = username
            session['user_id'] = person.id
            return redirect('/')
        except Exception as e:
            return f'Произошла ошибка {e}'
        
    else:
        return render_template('registration/signup.html')