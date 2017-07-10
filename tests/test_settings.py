import pytest
from os_tornado.settings import Settings


@pytest.fixture(scope="function")
def settings():
    return Settings()


def test_get_tornado_app_settings(settings):
    from os_tornado.settings import TORNADO_APP_SETTINGS_PREFIX
    from os_tornado.settings import get_tornado_app_settings
    key = TORNADO_APP_SETTINGS_PREFIX + "COOKIE_SECRET"
    settings[key] = 'random_string'
    assert get_tornado_app_settings(settings)['cookie_secret'] == settings[key]


def test_iter_overridden_settings(settings):
    from os_tornado.settings import iter_overridden_settings, default_settings
    settings.update_from_module(default_settings)
    count = 0
    for key, value in iter_overridden_settings(settings):
        count += 1
    assert count == 0
    settings["HTTP_PORT"] = 8000
    settings["LOG_ENABLE"] = True
    count = 0
    for key, value in iter_overridden_settings(settings):
        count += 1
    assert count == 1


def test_iter_default_settings(settings):
    from os_tornado.settings import default_settings
    settings.update_from_module(default_settings)
    for key in settings:
        assert getattr(default_settings, key) == settings[key]


TEST_KEY1 = 1
TEST_KEY2 = '2'
TEST_KEY3 = True
test_Key4 = [1, 2, 3]


def test_update_from_module(settings):
    settings.update_from_module('tests.test_settings')
    assert settings['TEST_KEY1'] == 1
    assert settings.get('TEST_KEY2') == '2'
    assert settings['TEST_KEY3']
    assert len(settings) == 3


def test_get(settings):
    test_cases = [
        # value , settings.get_x, expected, Exception
        (True, settings.get_bool, True, None),
        (1, settings.get_bool, True, None),
        (0, settings.get_bool, False, None),
        ('0', settings.get_bool, False, None),
        (None, settings.get_bool, False, TypeError),
        (1, settings.get_int, 1, None),
        ('1', settings.get_int, 1, None),
        ([1, 2, 3], settings.get_list, [1, 2, 3], None),
        ('1, 2,3', settings.get_list, ['1', '2', '3'], None),
        (1, settings.get_list, ['1', '2', '3'], TypeError),
        ({1: 1}, settings.get_dict, {1: 1}, None),
        ('{"1": 1}', settings.get_dict, {"1": 1}, None),
        (1.2, settings.get_float, 1.2, None),
        ("1.2", settings.get_float, 1.2, None),

    ]

    count = 0
    for value, get_method, expected, exception in test_cases:
        count += 1
        key = 'KEY%d' % count
        settings[key] = value
        if exception:
            with pytest.raises(exception):
                get_method(key)
        else:
            assert get_method(key) == expected


def test_set_item(settings):
    settings[1] = 1
    settings[1] = 2
    assert settings[1] == 2


def test_contain(settings):
    assert 1 not in settings
    settings[1] = 1
    assert 1 in settings


def test_len(settings):
    assert len(settings) == 0
    settings[1] = 1
    assert len(settings) == 1


def test_get_item(settings):
    settings[1] = 1
    assert settings.get(1) == 1
    assert settings.get(2) is None
    assert settings.get(2, 1) == 1


def test_delete_item(settings):
    settings[1] = 1
    assert settings[1] == 1
    del settings[1]
    assert settings[1] is None


def test_init_settings():
    d = {1: 1, 2: 2}
    s = Settings(d)
    assert d == s.attributes


def test_freeze(settings):
    settings[1] = 1
    settings.freeze()
    with pytest.raises(TypeError):
        settings[2] = 2
    with pytest.raises(TypeError):
        del settings[2]
