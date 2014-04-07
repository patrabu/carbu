# encoding: utf-8

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.httpauth import HTTPBasicAuth
from config import basedir, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USE_SSL, MAIL_USERNAME, MAIL_PASSWORD, ADMINS

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
auth = HTTPBasicAuth()

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler
    
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
        
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'noreply@' + MAIL_SERVER, ADMINS, 
        'carbu-api failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
    
    file_handler = RotatingFileHandler('tmp/carbu-api.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    app.logger.info('carbu-api startup...')

from app import views, models

