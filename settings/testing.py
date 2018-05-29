import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))


MODE = 'testing'
WORDLIST_FILEPATH = 'fixtures/wordlist.txt'
APP_NAME = 'shortly-testing'
DEBUG = True
TESTING = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR,
                                                      '../data-testing.sqlite')
