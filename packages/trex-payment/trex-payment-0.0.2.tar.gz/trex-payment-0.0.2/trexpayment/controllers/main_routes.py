'''
Created on 17 Sep 2020

@author: jacklok
'''

from flask import Blueprint, render_template, session, abort, redirect
from flask.helpers import url_for
import logging, jinja2


logger = logging.getLogger('root')

main_bp = Blueprint('main_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/')

main_bp.jinja_loader = jinja2.ChoiceLoader([
    main_bp.jinja_loader,
    jinja2.PackageLoader(__name__) 
])

@main_bp.route('/')
@main_bp.route('/home')
def home_page(): 
    logger.info('---home---')
    return render_template('index.html',
                           navigation_page = 'home'
                           )


@main_bp.route('/thank-you-onboard')
def thank_you_onboard_page(): 
    
    return render_template('thank_you_on_board.html',
                           home_page_url = url_for('main_bp.home_page')
                           )
    
           
    
