'''
Created on 20 Apr 2020

@author: jacklok
'''
import csv, os, json 
from flask import Blueprint, send_file
from trexpayment.conf import APP_LOGO_PATH
from trexpayment import conf
import logging

logger = logging.getLogger('root')

base_dir = os.path.abspath(os.path.dirname(conf.__file__))
    
templates_path      = os.path.join(base_dir, "templates")
static_path         = os.path.join(base_dir, "static")

custom_bp = Blueprint('custom_bp', __name__,
                     url_prefix         = '/custom'
                     )




@custom_bp.route('/app-logo.png', methods=['GET'])
def app_logo():
    logger.debug('---application logo---')
    logger.debug('APP_LOGO_PATH=%s', APP_LOGO_PATH)
    
    return send_file(static_path+'/'+APP_LOGO_PATH, mimetype='image/png')

 



