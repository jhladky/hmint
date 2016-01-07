from os import environ
from ast import literal_eval

DEBUG = bool(environ.get('DEBUG', False))
TESTING = bool(environ.get('TESTING', False))
