class Config:
    pass
    SECRET_KEY = 'monket'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'reilly.oduory@student.moringaschool.com'
    MAIL_PASSWORD = 'BitchIcode'

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost:5433/blog'
    DEBUG = True

class ProdConfig(Config):
    pass

config_options = {
    'development' : DevConfig,
    'production' : ProdConfig
}