from flask import Blueprint, render_template, request, redirect, session, url_for, current_app
from extensions import db
from models import Person, Post
import os
import uuid
from app.registration.registration import allowed_file
from werkzeug.utils import secure_filename

user_account = Blueprint('user_account', __name__, template_folder='templates')

@user_account.route('/')
def account():
    user_id = session.get('user_id')
    if user_id:
        try:
            user = Person.query.get(user_id) 
            return render_template('account/account.html', user=user)
        except Exception as e:
            return f'Ошибка {e}'
    return redirect(url_for('signin'))

@user_account.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@user_account.route('/create', methods=['POST', 'GET'])
def create():
    if 'user' in session:
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['text']

            if not title or not text:
                return render_template('account/create.html')
                

            post = Post(title=title, text=text, author_id=session['user_id'])

            try:
                db.session.add(post)
                db.session.commit()
                return redirect('/posts')
            except:
                return 'Произошла ошибка'
        else:
            return render_template('account/create.html')
    else:
        return redirect(url_for('index'))
    
@user_account.route('/change-avatar', methods=['POST'])
def change_avatar():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/signin')

    user = Person.query.get(user_id)
    if not user:
        return redirect('/signin')

    file = request.files.get('avatar')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4()}.{ext}"

        # удалить старый файл, если не default.png
        if user.avatar and user.avatar != 'default.png':
            try:
                os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], user.avatar))
            except FileNotFoundError:
                pass

        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name))
        user.avatar = unique_name
        db.session.commit()

    return redirect(url_for('user_account.account'))

