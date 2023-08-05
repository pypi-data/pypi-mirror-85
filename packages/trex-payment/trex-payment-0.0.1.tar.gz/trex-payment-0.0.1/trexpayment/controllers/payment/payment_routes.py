'''
Created on 5 Nov 2020

@author: jacklok
'''
from trexpayment.conf import STRIPE_WEBHOOK_END_POINT_SECRET_MAPPING, PAYMENT_GATEWAY_APP_KEY, PAYMENT_GATEWAY_SECRET_KEY,\
    STRIPE_CLIENT_ID, STRIPE_CONNECT_ONBOARD_REFRESH_URL, STRIPE_CONNECT_ONBOARD_RETURN_URL, STRIPE_CONNECT_ONBOARD_URL
from flask import Blueprint, render_template, session, abort, redirect, jsonify, request, Response
from flask.helpers import url_for
import stripe
import logging



stripe_keys = {
  'secret_key'      : PAYMENT_GATEWAY_SECRET_KEY,
  'publishable_key' : PAYMENT_GATEWAY_APP_KEY,
  'client_id'       : STRIPE_CLIENT_ID,
}

stripe.api_key          = stripe_keys['secret_key']
stripe.client_id        = stripe_keys['client_id']


STRIPE_PUBLISHABLE_KEY = PAYMENT_GATEWAY_APP_KEY


payment_bp = Blueprint('payment_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/payment')


@payment_bp.route('/success', methods=['GET'])
def paid_success():
        
    request_params = request.args
    
    logging.debug('request_params=%s', request_params)
    
    return render_template("payment/success_payment.html", 
                           receipt_url = None
                           )    
