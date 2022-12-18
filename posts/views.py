from flask import Blueprint, render_template
from .dao.posts_dao import PostDAO

posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')
post_dao = PostDAO('data/posts.json')


@posts_blueprint.route('/')
def main_page():
    posts = post_dao.get_all_posts()
    return render_template('index.html', posts=posts)

@posts_blueprint.route('/posts/<int:post_id>')
def post_id_page(post_id):
    post = post_dao.get_post_by_pk(post_id)
    comments = post_dao.get_comments_by_post_id(post_id)
    return render_template('post.html', post=post, comments=comments, amount_comments=len(comments))
