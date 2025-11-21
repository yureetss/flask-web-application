from flask import Blueprint, render_template, request, redirect, session, url_for
from extensions import db
from models import Person

authentification = Blueprint('authentification', __name__, template_folder='templates')

@authentification.route('/signin', methods= ['POST', 'GET'])
def signin():
    if 'user' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Person.query.filter_by(username=username).first()
        
        if user and user.check_password(password):

            try:
                db.session.commit()
                session['user'] = user.username
                session['user_id'] = user.id
                return redirect('/')
            except Exception as e:
                return f'Произошла ошибка {e}'
            
        if user is None or not user.check_password(password):
            error_incorrect = 'Неверное имя пользователя или пароль'
            return render_template('authentification/signin.html', error_incorrect=error_incorrect)
        
        else:
            return render_template('authentification/signin.html')
        
    else:
        return render_template('authentification/signin.html')