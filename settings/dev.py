import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

MODE = 'dev'
WORDLIST_FILEPATH = 'fixtures/wordlist.txt'
APP_NAME = 'shortly-dev'
DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR,
                                                      '../data-dev.sqlite')
