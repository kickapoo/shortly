from app.factory import create_app


def test_dev_config():
    app = create_app('dev')
    assert app.config['MODE'] == 'dev'
    assert app.config['DEBUG']
    assert not app.config['TESTING']


def test_testing_config():
    app = create_app('testing')
    assert app.config['MODE'] == 'testing'
    assert app.config['DEBUG']
    assert app.config['TESTING']


def test_prod_config():
    app = create_app('prod')
    assert app.config['MODE'] == 'prod'
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
