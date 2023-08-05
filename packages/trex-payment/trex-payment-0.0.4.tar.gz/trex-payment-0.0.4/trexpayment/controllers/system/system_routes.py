'''
Created on 20 Apr 2020

@author: jacklok
'''
import csv, os, json 
from flask import Blueprint, render_template, request, current_app, session
from trexlib.utils.log_util import get_tracelog
from trexweb.utils.common.http_response_util import create_cached_response, MINE_TYPE_JSON, MINE_TYPE_JAVASCRIPT
from trexlib.utils.common.common_util import sort_dict_list
from trexmodel.utils.model.model_util import create_db_client
from trexweb.libs.http import StatusCode, create_rest_message 
from trexpayment.conf import APP_LOADING_PATH
import logging
from flask.helpers import url_for



system_bp = Blueprint('system_bp', __name__,
                     template_folder    = 'templates',
                     static_folder      = 'static',
                     url_prefix         = '/system'
                     )


@system_bp.after_request
def set_system_response_headers(response):
    request_url = request.url
    logging.debug('request_url=%s', request_url)
    
    if request_url.endswith('.js'):
        response.headers['Content-Type'] = MINE_TYPE_JAVASCRIPT
    
    response.charset= 'utf-8'    
    logging.debug('---set_system_response_headers---')
    
    return response



@system_bp.route('/config.js', methods=['GET'])
def config():
    logging.debug('############################### config ############################### ')
    
    config_dict = {
                    "LOADING_IMAGE_PATH"    : url_for('static', filename=APP_LOADING_PATH),
                    "LOADING_TEXT"          :'Please wait, your request are processing now', 
                    }
    
    
    return render_template("system/config.js", **config_dict)

@system_bp.route('/js-i18n.js', methods=['GET'])
def javascript_i18n_message():
    logging.debug('---javascript_i18n_message--- ')
    return render_template("i18n/js_message.js")

@system_bp.route('/app-logo.png', methods=['GET'])
def app_logo():
    logging.debug('---application logo--- ')
    return render_template("i18n/js_message.js")

 



