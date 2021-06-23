from flask import render_template, url_for, redirect, abort, request
from flask_login import login_required, current_user
from .. import db
from ..models import User, Post, Comment
from . import main
from .forms import PostForm, CommentForm


@main.route("/")
def index():
    title = 'Welcome'
    posts = Post.get_all_posts()

    search_post = request.args.get('post_query')

    if search_post:
        return redirect(url_for('main.search', post_name=search_post))
    else:
        return render_template('index.html', title=title, posts=posts)


@main.route("/profile/<uname>")
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    posts = Post.user_specific_posts(user.id)

    if user is None:
        abort(404)

    return render_template('profile/profile.html', user=user, posts=posts)


@main.route("/post/<int:post_id>")
def fullpost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    comments = Comment.get_post_specific_comment(post_id)
    username = db.select([User.username]).where(User.id == Comment.user_id)

    if post is None:
        abort(404)

    return render_template('post.html', post=post, comments=comments, username=username)


@main.route("/post/like/<int:post_id>", methods=["GET","POST"])
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        abort(404)

    post.likes = post.likes + 1
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('main.fullpost', post_id=post.id))


@main.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(current_user.id, form.title.data, form.content.data)

        Post.save_post(post)
        return redirect(url_for('main.profile', uname=current_user.username))

    return render_template('new_post.html', form=form)


@main.route("/post/comment/new/<int:post_id>", methods = ["GET", "POST"])
@login_required
def new_comment(post_id):
    form = CommentForm()
    post = Post.query.filter_by(id=post_id).first()
    if form.validate_on_submit():
        comment = Comment(current_user.id, post.id, form.comment.data)
        Comment.save_comment(comment)
        return redirect(url_for('main.fullpost', post_id=post.id))

    title = 'New Comment'
    return  render_template('new_comment.html',form=form,post=post,title=title)


@main.route("/search/<post_name>")
def search(post_name):
    results = Post.search_post(post_name)
    title = f'search results for {post_name}'

    return render_template('search.html', results=results, title=title)