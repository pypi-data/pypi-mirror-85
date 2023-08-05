'''
Created on 4 Nov 2020

@author: jacklok
'''

from flask import Flask, render_template, current_app, url_for, request, g, abort, request, session
import sys, os, base64, json, logging
from trexlib.utils.common.cache_util import cache
from trexmodel.utils.model.model_util import read_service_account_file, create_db_client
from trexmodel.models.datastore.user_models import User, LoggedInUser
from trexmodel.models.datastore.admin_models import SuperUser, AdminUser
from trexlib import conf
from trexpayment import conf as payment_conf
from trexlib.utils.common.common_util import id_generator
from trexlib.utils.common.user_util import get_gravatar_url
from trexlib.utils.string_util import is_empty, is_not_empty
from logging import config
from flask_google_cloud_logger import FlaskGoogleCloudLogger
from flask_babel import Babel

logger = logging.getLogger('root')
logger.setLevel(payment_conf.LOGGING_LEVEL)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)
 
def create_app():
    print('---create_app--')
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    translation_path    = os.path.join(base_dir, "translations")
    templates_path      = os.path.join(base_dir, "trexpayment/templates")
    static_path         = os.path.join(base_dir, "trexpayment/static")
    
    print('base_dir=', base_dir)
    print('translation_path=', translation_path)
    print('templates_path=', templates_path)
    print('static_path=', static_path)
    
    app = Flask(__name__, template_folder=templates_path)
    
    app.static_folder=static_path
    
    with app.app_context():
        
        credential_filepath                         = 'gae-service-account-key.json'
        (database_config, data)                     = read_service_account_file(credential_filepath=credential_filepath)
        
        app.config['DEBUG']                         = payment_conf.DEBUG_MODE
        app.config['SECRET_KEY']                    = conf.SECRET_KEY
        app.config['OAUTH_CREDENTIALS']             = {
                                                    }
        app.config['LANGUAGES']                     = conf.SUPPORT_LANGUAGES
        
        app.config['database_config']               = database_config
        
        
    return app

app                                 = create_app()
app.config['version_no']            = id_generator()

#config.dictConfig(payment_conf.LOG_CONFIG)

#FlaskGoogleCloudLogger(app)

#logger.setLevel(logging.DEBUG)

#handler = logging.StreamHandler(sys.stdout)

#app.logger.addHandler(handler)

babel = Babel(app)

@babel.localeselector
def get_locale():
    logger.debug('request.accept_languages=%s', request.accept_languages)
    return request.accept_languages.best_match(app.config['LANGUAGES'])

'''
Application settings here
'''
@app.context_processor
def inject_settings():
    
    
    return dict(
                application_title           = payment_conf.APPLICATION_TITLE, 
                application_name            = payment_conf.APPLICATION_NAME,
                application_desc            = payment_conf.APPLICATION_DESC,
                application_logo            = payment_conf.APP_LOGO_PATH,
                DEBUG_MODE                  = 'true' if payment_conf.DEBUG_MODE else 'false',
                APPLICATION_VERSION_NO      = os.environ.get('APPLICATION_VERSION_NO') or payment_conf.APPLICATION_VERSION_NO,
                DEPLOYED_VERSION_NO         = current_app.config['version_no'],
                )

from trexpayment.controllers.main_routes import main_bp
from trexpayment.controllers.integration.integrate_routes import integrate_bp
from trexpayment.controllers.event.event_routes import event_bp
from trexpayment.controllers.integration.checkout_routes import checkout_bp
from trexpayment.controllers.system.system_routes import system_bp
from trexpayment.controllers.system.custom_routes import custom_bp

app.register_blueprint(main_bp)
app.register_blueprint(event_bp)
app.register_blueprint(integrate_bp)
app.register_blueprint(checkout_bp)
app.register_blueprint(system_bp)
app.register_blueprint(custom_bp)

logger.info('---added module--')

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8083, debug=True)
