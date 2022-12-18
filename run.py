from flask import Flask, render_template
from posts.views import posts_blueprint

app = Flask(__name__)

app.register_blueprint(posts_blueprint)

# @app.route('/')
# def main_page():
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
