#!flask/bin/python
# -*- coding: utf-8 -*

import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'carbu.sqlite')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DATETIME_FMT = '%Y-%m-%d %H:%M:%S'
CRSF_ENABLED = True
SECRET_KEY = 'tu-ne-devineras-jamais'
LAST_REFILLS = 50

# Mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_SSL = False
MAIL_USE_TLS = False
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['webmaster@rabu.fr']
