import pytest

from posts.dao.posts_dao import PostDAO


@pytest.fixture()
def post_dao():
    post_dao_test = PostDAO('data/posts.json')
    return post_dao_test

posts_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count","likes_count","pk"}


class TestPostsDAO:

    def test_get_all_posts(self, post_dao):
        posts = post_dao.get_all_posts()

        assert type(posts) == list, 'Возвращается не список'
        assert len(posts) > 0, 'Возвращается пустой список'
        assert set(posts[0].keys()) == posts_keys, 'Возвращается неверный список ключей'

    def test_one_post(self, post_dao):
        post = post_dao.get_post_by_pk(1)
        assert type(post) == dict, 'Возвращается не список'
        assert post['pk'] == 1, 'Возвращается пост с неправильным pk'

        post = post_dao.get_post_by_pk(1000000000000)
        assert post == dict(), 'Возвращается непустой словарь при несуществующем id'

        with pytest.raises(TypeError):
            post_dao.get_post_by_pk('один')

    def test_get_user_posts(self, post_dao):
        posts = post_dao.get_user_posts('leo')
        assert type(posts) == list, 'Возвращается не список'
        assert len(posts) > 0, 'Возвращается пустой список'

        posts = post_dao.get_user_posts('hanna')
        assert len(posts) == 0, 'Возвращается не пустой список'

        with pytest.raises(ValueError):
            post_dao.get_user_posts('no_name')

    def test_search_for_posts(self, post_dao):
        posts = post_dao.search_for_posts('кот')
        assert type(posts) == list, 'Возвращается не список'
        assert len(posts) > 0, 'Ошибка поиска по слову кот'

        posts = post_dao.search_for_posts('КоТ')
        assert len(posts) > 0, 'Ошибка поиска по слову КоТ'

        posts = post_dao.search_for_posts('вомиываыоватлывм')
        assert len(posts) == 0, 'Ошибка поиска по несуществующему слову'

    def test_get_comments_by_post_id(self, post_dao):
        comments = post_dao.get_comments_by_post_id(1)
        assert type(comments) == list, 'Возвращается не список'
        assert len(comments) > 0, 'Возвращается пустой список'

        with pytest.raises(ValueError):
            post_dao.get_comments_by_post_id(-5)
