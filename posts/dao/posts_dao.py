import json


class PostDAO:
    """
    Класс для работы с данными
    """

    def __init__(self, path):
        self.posts_path = path
        self.users_path = 'data/users.json'
        self.comments_path = 'data/comments.json'
        self.bookmarks_path = 'data/bookmarks.json'

    def load_data(self, path):
        """
        Загружает данные из файла
        :param path: ссылка на json файл
        :return: list
        """
        with open(path, encoding='utf-8') as file:
            posts = json.load(file)

        return posts

    def load_posts(self) -> list:
        """
        Загружает все посты
        :return: list
        """
        return self.load_data(self.posts_path)

    def load_users(self) -> list:
        """
        Загружает всех пользователей
        :return: list
        """
        return self.load_data(self.users_path)

    def load_comments(self) -> list:
        """
        Загружает все комментарии
        :return: list
        """
        return self.load_data(self.comments_path)

    def load_bookmarks(self) -> list:
        """
        Загружает все закладки
        :return: list
        """
        return self.load_data(self.bookmarks_path)

    def save_bookmarks(self, bookmarks: list) -> None:
        """
        Сохраняет закладки в json - файл
        :param bookmarks: список закладок
        :return: None
        """
        with open(self.bookmarks_path, 'w', encoding='utf-8') as file:
            json.dump(bookmarks, file)

    def get_all_posts(self) -> list:
        """
        Возвращает все посты
        :return: list
        """
        posts = self.load_posts()
        return posts

    def get_user_posts(self, user_name: str) -> list:
        """
        Возвращает все посты пользователя с ником user_name
        :param user_name: ник пользователя
        :return: list
        """
        users = self.load_users()
        if user_name not in users:
            raise ValueError(f'{user_name} is not user')

        posts = self.load_posts()
        user_posts = [post for post in posts if post['poster_name'] == user_name]

        return user_posts

    def get_comments_by_post_id(self, post_id: int) -> list:
        """
        Возвращает все комментарии под постом с id post_id
        :param post_id: id поста, под которым нужны комментарии
        :return: list
        """
        posts_id = [post['pk'] for post in self.load_posts()]
        if post_id not in posts_id:
            raise ValueError(f"post with id{post_id} doesn't exist")

        comments = self.load_comments()
        post_comments = [comment for comment in comments if comment['post_id'] == post_id]

        return post_comments

    def search_for_posts(self, query: str) -> list:
        """
        Осуществляет поиск в постах по слову "query"
        :param query: слово для поиска
        :return: list
        """
        posts = self.load_posts()
        query = query.lower()
        post_with_query = [post for post in posts if query in post['content'].lower()]

        return post_with_query

    def get_post_by_pk(self, pk: int) -> dict:
        """
        Возвращает пост с id = 'pk'
        :param pk: id номер поста
        :return: dict
        """
        if type(pk) != int:
            raise TypeError(f'{pk} is not digit')

        for post in self.load_posts():
            if post['pk'] == pk:
                return self.add_hashtags(post)

        return dict()

    def add_hashtags(self, post: dict) -> dict:
        """
        Создает ссылки из хэштегов
        :param post: пост пользователя
        :return: dict
        """
        if '#' in post['content']:
            content_split = post['content'].split()

            for i, word in enumerate(content_split):
                if word[0] == '#':
                    new_word = f'<a href="/tag/{word[1:]}">#{word[1:]}</a>'
                    content_split[i] = new_word

            post['content'] = (' ').join(content_split)

        return post

    def add_bookmark(self, post_id: int) -> None:
        """
        Добавляет пост в закладки
        :param post_id: id поста
        :return: None
        """
        bookmarks = self.load_bookmarks()
        bookmarks.append(post_id)
        self.save_bookmarks(bookmarks)

    def remove_bookmark(self, post_id: int) -> None:
        """
        Удаляет пост из закладок
        :param post_id: id поста
        :return: None
        """
        bookmarks = self.load_bookmarks()
        bookmarks.remove(post_id)
        self.save_bookmarks(bookmarks)

    def is_in_bookmarks(self, post_id: int) -> bool:
        """
        Проверяет есть ли пост в закладках
        :param post_id:
        :return:
        """
        bookmarks = self.load_bookmarks()
        return post_id in bookmarks

    def get_posts_in_bookmarks(self) -> list:
        """
        Возвращает посты, которые находятся в закладках
        :return: list
        """
        bookmarks = self.load_bookmarks()
        posts = [post for post in self.load_posts() if post['pk'] in bookmarks]

        return posts

    def get_amount_bookmarks(self) -> int:
        """
        Возвращает количество закладок
        :return: int
        """
        bookmarks = self.load_bookmarks()
        return len(bookmarks)
