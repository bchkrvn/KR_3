import json


class PostDAO:

    def __init__(self, path):
        self.posts_path = path
        self.users_path = 'data/users.json'
        self.comments_path = 'data/comments.json'


    def load_posts(self) -> list:
        with open(self.posts_path, encoding='utf-8') as file:
            posts = json.load(file)

        return posts

    def load_users(self) -> list:
        with open(self.users_path, encoding='utf-8') as file:
            users = json.load(file)

        return users

    def load_comments(self) -> list:
        with open(self.comments_path, encoding='utf-8') as file:
            users = json.load(file)

        return users

    def get_all_posts(self) -> list:
        posts = self.load_posts()
        return posts

    def get_user_posts(self, user_name: str) -> list:
        users = self.load_users()
        if user_name not in users:
            raise ValueError(f'{user_name} is not user')

        posts = self.load_posts()
        user_posts = [post for post in posts if post['poster_name'] == user_name]

        return user_posts

    def get_comments_by_post_id(self, post_id: int) -> list:
        posts_id = [post['pk'] for post in self.load_posts()]
        if post_id not in posts_id:
            raise ValueError(f"post with id{post_id} doesn't exist")

        comments = self.load_comments()
        post_comments = [comment for comment in comments if comment['post_id'] == post_id]

        return post_comments

    def search_for_posts(self, query) -> list:
        posts = self.load_posts()
        query = query.lower()
        post_with_query = [post for post in posts if query in post['content'].lower()]

        return post_with_query

    def get_post_by_pk(self, pk: int) -> dict:
        if type(pk) != int:
            raise TypeError(f'{pk} is not digit')

        for post in self.load_posts():
            if post['pk'] == pk:
                return post

        return dict()

