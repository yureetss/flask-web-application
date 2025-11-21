from flask import Blueprint, render_template, session, redirect, request, url_for, abort
from models import Post, Person, Comment
from extensions import db

records = Blueprint('records', __name__, template_folder='templates')

@records.route('/posts')
def posts():
    
    posts = Post.query.all()
    return render_template('records/posts.html', posts=posts)

    
@records.route('/record/<int:id>', methods=['GET', 'POST'])
def record(id):
    post = Post.query.get_or_404(id)

    # Добавление комментария
    if request.method == 'POST':
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/signin')

        text = request.form.get('comment_text', '').strip()
        if text:
            comment = Comment(text=text, post_id=post.id, user_id=user_id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('records.record', id=id))

    comments = Comment.query.filter_by(post_id=id).order_by(Comment.created_at.asc()).all()
    return render_template('records/record.html', post=post, comments=comments)

@records.route('/comment/delete/<int:comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    user_id = session.get('user_id')
    if not user_id:
        return redirect('/signin')

    # Разрешаем удаление:
    # - автору комментария
    # - автору поста
    if user_id != comment.user_id and user_id != comment.post.author_id:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('records.record', id=comment.post_id))

@records.route('/author/<string:username>')
def author_page(username):
    if 'user' in session:
        author = Person.query.filter_by(username=username).first_or_404()
        return render_template('records/author.html', author=author)
    else:
        return redirect('/signin')
