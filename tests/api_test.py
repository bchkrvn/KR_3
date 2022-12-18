from run import app


posts_keys = {"poster_name", "poster_avatar", "pic", "content", "views_count","likes_count","pk"}


class TestAPI:

    def test_get_all_posts(self):
        response = app.test_client().get('/api/posts')
        assert type(response.json) == list, 'Возвращается не список'
        assert len(response.json) > 0, 'Возвращается пустой список'
        assert set(response.json[0].keys()) == posts_keys, 'Возвращаются неправильные ключи'

    def test_get_one_post(self):
        response = app.test_client().get('/api/posts/1')
        assert type(response.json) == dict, 'Возвращается не словарь'
        assert set(response.json.keys()) == posts_keys, 'Возвращаются неправильные ключи'
