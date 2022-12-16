"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()


@app.route('/')
def home():
    posts = Post.query.order_by(Post.create_at.desc()).all()

    return render_template('homepage.html', posts=posts)


@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users = users)


@app.route('/users/new', methods=['GET'])
def show_form():
    
    return render_template('users_new.html')


@app.route('/users/new', methods=['POST'])
def add_new_user():
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def show_detail(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('users_detail.html', user = user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('users_edit.html', user = user)



@app.route('/users/<int:user_id>/edit', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['new_first_name']
    user.last_name = request.form['new_last_name']
    user.image_url = request.form['new_image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')



# posts routes
@app.route('/users/<int:user_id>/posts/new')
def post_new_form(user_id):

    user = User.query.get_or_404(user_id)

    return render_template('post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user_id=user.id)

    db.session.add(new_post)
    db.session.commit()
    flash(f'Post "{new_post.title}" added.')

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template('post_detail.html', post = post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post_edit.html', post = post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edit(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f'Post "{post.title}" edited.')

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f'Post "{post.title}" deleted.')

    return redirect(f"/users/{post.user_id}")




