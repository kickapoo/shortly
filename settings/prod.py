import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))


MODE = 'prod'
WORDLIST_FILEPATH = 'fixtures/wordlist.txt'
APP_NAME = 'shortly - Yet another shorten url service'
DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR,
                                                      '../data-prod.sqlite')
