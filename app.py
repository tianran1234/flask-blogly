"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post, Tag, PostTag
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
    users = User.query.order_by(User.last_name, User.first_name).all()
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

    flash(f'User {new_user.full_name} added.')

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

    flash(f'User {user.full_name} edited.')

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.full_name} deleted.')

    return redirect('/users')



# posts routes
@app.route('/users/<int:user_id>/posts/new')
def post_new_form(user_id):

    user = User.query.get_or_404(user_id)
    
    tags = Tag.query.all()

    return render_template('post_form.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user_id=user.id,
                    tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash(f'Post "{new_post.title}" added.')

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):

    post = Post.query.get_or_404(post_id)

    tags = post.tags

    return render_template('post_detail.html', post = post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post_edit.html', post = post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edit(post_id):

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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


# tags routes
@app.route('/tags/new')
def create_tag_form():
    
    posts = Post.query.all()

    return render_template('tag_form.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def submit_a_tag():

    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['tagname'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    flash(f'Tag "{new_tag.name}" added.')

    return redirect('/tags')



@app.route('/tags')
def list_tags():
    
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_detail.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tag_edit_form(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tag_edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tagname']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    flash(f'Tag "{tag.name}" edited.')

    return redirect(f'/tags')



@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')







