import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'a2plcpnl0268.prod.iad2.secureserver.net'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1 != None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'microblog@jakoblangseth.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'Heoft344!'
    ADMINS = ['microblog@jakoblangseth.com', 'jakob.langseth@gmail.com']
    POSTS_PER_PAGE=12
    LANGUAGES = ["en", "es", "nb"]
    MS_TRANSLATOR_KEY = "f0f08bb5ad8d44a8b774e085296ee02d"
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')