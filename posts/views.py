import logging
from flask import Blueprint, render_template, request, abort, jsonify, redirect
from .dao.posts_dao import PostDAO


posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')
post_dao = PostDAO('data/posts.json')
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    filename="api.log", level=logging.INFO, encoding='utf-8')


@posts_blueprint.route('/')
def main_page():
    try:
        posts = post_dao.get_all_posts()
        amount_bookmarks = post_dao.get_amount_bookmarks()
        return render_template('index.html', posts=posts,bookmarks=amount_bookmarks)
    except FileNotFoundError:
        abort(500)


@posts_blueprint.route('/posts/<int:post_id>')
def post_id_page(post_id):
    try:
        post = post_dao.get_post_by_pk(post_id)
        comments = post_dao.get_comments_by_post_id(post_id)
        return render_template('post.html', post=post, comments=comments, amount_comments=len(comments))
    except ValueError:
        abort(404)
    except FileNotFoundError:
        abort(500)


@posts_blueprint.route('/users/<user_name>')
def user_page(user_name):
    try:
        user_posts = post_dao.get_user_posts(user_name)
        return render_template('user-feed.html', posts=user_posts)
    except ValueError:
        abort(404)
    except FileNotFoundError:
        abort(500)


@posts_blueprint.route('/search/')
def search_page():
    try:
        query = request.args.get('s')
        posts = post_dao.search_for_posts(query)
        return render_template('search.html', posts=posts, posts_amount=len(posts), query=query)
    except FileNotFoundError:
        abort(500)


@posts_blueprint.route('/tag/<tagname>')
def tag_page(tagname):
    query = '#' + tagname
    posts = post_dao.search_for_posts(query)
    return render_template('tag.html', posts=posts, tagname=tagname, posts_amount=len(posts))


@posts_blueprint.route('/bookmarks/<int:post_id>')
def add_bookmark(post_id):
    if post_dao.is_in_booksmarks(post_id):
        return redirect(f'/bookmarks/remove/{post_id}', code=302)
    else:
        post_dao.add_booksmark(post_id)
        return redirect('/', code=302)


@posts_blueprint.route('/bookmarks/remove/<int:post_id>')
def remove_bookmark(post_id):
    post_dao.remove_bookmark(post_id)
    return redirect('/', code=302)


@posts_blueprint.route('/bookmarks')
def bookmarks():
    posts = post_dao.get_posts_in_bookmarks()
    return render_template('bookmarks.html', posts=posts)


@posts_blueprint.route('/api/posts')
def get_api_posts():
    logging.info('Обращение к /api/posts')
    posts = post_dao.get_all_posts()
    return jsonify(posts)


@posts_blueprint.route('/api/posts/<int:post_id>')
def get_api_post(post_id):
    posts = post_dao.get_post_by_pk(post_id)
    logging.info(f'Обращение к /api/posts/{post_id}')
    return jsonify(posts)


@posts_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@posts_blueprint.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

