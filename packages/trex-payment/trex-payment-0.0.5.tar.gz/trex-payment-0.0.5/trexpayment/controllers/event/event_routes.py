'''
Created on 6 Nov 2020

@author: jacklok
'''

from trexpayment.conf import PAYMENT_GATEWAY_APP_KEY, PAYMENT_GATEWAY_SECRET_KEY,\
    STRIPE_CLIENT_ID
from flask import Blueprint, render_template, session, abort, redirect, jsonify, request, Response
from flask.helpers import current_app
import stripe
import logging, json
from trexpayment.decorators.stripe_webhook_decorators import stripe_webhook_event_secret_verify
from trexpayment.models.datastore.payment_models import PaymentPaid, ChargeSucceeded
from trexmodel.utils.model.model_util import create_db_client
from trexlib.utils.log_util import get_tracelog

stripe_keys = {
  'secret_key'      : PAYMENT_GATEWAY_SECRET_KEY,
  'publishable_key' : PAYMENT_GATEWAY_APP_KEY,
  'client_id'       : STRIPE_CLIENT_ID,
}

stripe.api_key          = stripe_keys['secret_key']
stripe.client_id        = stripe_keys['client_id']


STRIPE_PUBLISHABLE_KEY = PAYMENT_GATEWAY_APP_KEY


event_bp = Blueprint('event_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/event')


logger = logging.getLogger('root')


@event_bp.route('/payout-paid', methods=['POST', 'GET'])
@stripe_webhook_event_secret_verify('payout.paid')
def payout_paid():
    
    logger.debug('event handling for payout paid')
    
    payload         = request.data.decode("utf-8")
    
    payload_json    = json.loads(payload)
    
    logger.debug('payload_json=%s', payload_json)
    if payload_json:
        transaaction_id     = payload_json.get('id')
        transaction_payload = payload_json.get('data').get('object')
        
        
        request_url = request.url
        
        db_client = create_db_client(info=current_app.config['database_config'], caller_info=request_url+":payout_paid")
        with db_client.context():
            
            PaymentPaid.create(transaaction_id, transaction_payload)
    
    return  Response(status=200)

@event_bp.route('/charge-succeeded', methods=['POST', 'GET'])
@stripe_webhook_event_secret_verify('charge.succeeded')
def charge_succeeded():
    
    logger.debug('event handling for charge succeeded')
    
    payload         = request.data.decode("utf-8")
    
    payload_json    = json.loads(payload)
    
    logger.debug('payload_json=%s', payload)
    if payload_json:
        try:
            transaaction_id         = payload_json.get('id')
            transaction_payload     = payload_json.get('data').get('object')
            receipt_url             = transaction_payload.get('receipt_url')
            metadata                = transaction_payload.get('metadata')
            invocie_no              = None
            merchant_acct_key       = None
            client_reference_no     = None
            
            
            if metadata:
                invoice_no              = metadata.get('invoice_no')
                merchant_acct_key       = metadata.get('merchant_acct_key')
                client_reference_no     = metadata.get('client_reference_no')
            
            logger.debug('invocie_no=%s', invocie_no)
            logger.debug('merchant_acct_key=%s', merchant_acct_key)
            logger.debug('client_reference_no=%s', client_reference_no)
            logger.debug('receipt_url=%s', receipt_url)
            
            request_url = request.url
            
            db_client = create_db_client(info=current_app.config['database_config'], caller_info=request_url+":charge_succeeded")
            with db_client.context():
                
                PaymentPaid.create(transaaction_id, merchant_acct_key, transaction_payload, 
                                   invoice_no=invoice_no, receipt_url=receipt_url,
                                   client_reference_no=client_reference_no)
        except:
            logger.error(get_tracelog())
            return  Response(status=400)
    
    return  Response(status=200)   



@event_bp.route('/charge-session-payment-completed', methods=['POST', 'GET'])
@stripe_webhook_event_secret_verify('checkout.session.async_payment_succeeded')
def charge_session_async_payment_completed():
    
    logger.debug('event handling for checkout.session.async_payment_succeeded')
    
    payload         = request.data.decode("utf-8")
    
    logger.debug('payload_json=%s', payload)
    
    
    return  Response(status=200)

