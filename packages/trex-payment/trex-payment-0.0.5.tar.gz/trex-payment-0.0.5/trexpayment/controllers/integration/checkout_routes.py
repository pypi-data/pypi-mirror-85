'''
Created on 5 Nov 2020

@author: jacklok
'''

from trexpayment.conf import PAYMENT_GATEWAY_APP_KEY, PAYMENT_GATEWAY_SECRET_KEY,\
    STRIPE_CLIENT_ID, SUPPORT_EMAIL
from flask import Blueprint, render_template, session, abort, redirect, jsonify, request, Response
from flask.helpers import url_for
from trexpayment.product_conf import PRODUCT_DETAILS
from trexpayment.conf import SUPPORTED_LANGUAGE, PAYMENT_SUCCESS_URL, PAYMENT_CANCEL_URL
from trexpayment.models.datastore.payment_models import ChargeSucceeded,\
    PaymentPaid
from trexmodel.utils.model.model_util import create_db_client
from flask.helpers import current_app
import stripe
import logging, jinja2
from trexlib.utils.string_util import is_not_empty
from trexpayment.util.invoice_util import generate_invoice_no
#from trexlib.utils.crypto_util import encrypt, decrypt

logger = logging.getLogger('root')

stripe_keys = {
  'secret_key'      : PAYMENT_GATEWAY_SECRET_KEY,
  'publishable_key' : PAYMENT_GATEWAY_APP_KEY,
  'client_id'       : STRIPE_CLIENT_ID,
}

stripe.api_key          = stripe_keys['secret_key']
stripe.client_id        = stripe_keys['client_id']


STRIPE_PUBLISHABLE_KEY = PAYMENT_GATEWAY_APP_KEY


checkout_bp = Blueprint('checkout_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/checkout')

checkout_bp.jinja_loader = jinja2.ChoiceLoader([
    checkout_bp.jinja_loader,
    jinja2.PackageLoader(__name__) 
])


@checkout_bp.route("/create/<product_code>/merchant_acct/<merchant_acct_key>")
def create(product_code, merchant_acct_key):
    
    product_details = None
    
    logger.info('product_code=%s', product_code)
    logger.info('merchant_acct_key=%s', merchant_acct_key)
    
    if is_not_empty(product_code) and is_not_empty(merchant_acct_key):
    
        
        product_code    = product_code.lower()
        
        product_details_in_language_dict = PRODUCT_DETAILS.get(product_code)
        
        if product_details_in_language_dict:
            lang = request.accept_languages.best_match(SUPPORTED_LANGUAGE)
            
            logging.info('lang=%s', lang)
            
            product_details = product_details_in_language_dict.get(lang)
                
                
        if product_details:
            invoice_no = generate_invoice_no()
            
            logger.info('invoice_no=%s', invoice_no)
            
            session = stripe.checkout.Session.create(
                                    payment_method_types    = ['card'],
                                    line_items              = [product_details],
                                    mode                    = 'payment',
                                    success_url             = PAYMENT_SUCCESS_URL,
                                    cancel_url              = PAYMENT_CANCEL_URL,
                                    client_reference_id     = merchant_acct_key,
                                    metadata                = {
                                                                'merchant_acct_key' : merchant_acct_key,
                                                                'product_code'      : product_code,
                                                                'invoice_no'        : invoice_no,
                                                                },
                                    payment_intent_data     = {
                                                                'metadata': {
                                                                    'merchant_acct_key': merchant_acct_key,
                                                                    'product_code'      : product_code,
                                                                    'invoice_no'        : invoice_no,
                                                                }
                                                        }
                                    )
            
            if session:
                logger.info('session.id=%s', session.id)
                
                return render_template("checkout/create_checkout.html", 
                               payment_key      = STRIPE_PUBLISHABLE_KEY,
                               session_id       = session.id,    
                               )
        
    
    return '',400

@checkout_bp.route('/payment-success', methods=['GET'])
def payment_success():
    session_id          = request.args.get('session_id')
    view_receipt_url    = None
    if is_not_empty(session_id):
        session = stripe.checkout.Session.retrieve(session_id)
        if session:
            metadata = session.metadata
            if metadata:
                invoice_no = metadata.get('invoice_no')
                if is_not_empty(invoice_no):
                    #encrypted_invoice_no    = encrypt(invoice_no)
                    encrypted_invoice_no    = invoice_no   
                    view_receipt_url        = url_for('checkout_bp.read_receipt', encrypted_invoice_no=encrypted_invoice_no)        
            
            
    return render_template("checkout/payment_success.html",
                           support_email    = SUPPORT_EMAIL,
                           view_receipt_url = view_receipt_url 
                           )    
    
@checkout_bp.route('/payment-cancel', methods=['GET'])
def payment_cancel():
    
    return render_template("checkout/payment_cancel.html", 
                           )
    
@checkout_bp.route('/charge-succeeded/<transaction_id>', methods=['GET'])
def read_charge_succeeded(transaction_id):
    request_url = request.url
    db_client = create_db_client(info=current_app.config['database_config'], caller_info=request_url+":charge_succeeded")
    with db_client.context():
        charge_succeeded = ChargeSucceeded.read(transaction_id)
    if charge_succeeded:
        return jsonify({
                    'transaction_id'    : transaction_id,
                    'charged_datetime'  : charge_succeeded.charged_datetime,
                    'payload'           : charge_succeeded.transaction_payload,    
                    }) 
    else:
        abort(400)
        
@checkout_bp.route('/retrieve-charge-succeeded/<charge_id>', methods=['GET'])
def retrieve_charge_succeeded(charge_id):
    charge_succeeded = stripe.Charge.retrieve(charge_id)
    
    if charge_succeeded:
        return jsonify(charge_succeeded)
    
    abort(400)  
    
@checkout_bp.route('/retrieve-session/<session_id>', methods=['GET'])
def retrieve_session(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    
    if session:
        return jsonify(session)
    
    abort(400)
    
@checkout_bp.route('/read-receipt/<encrypted_invoice_no>', methods=['GET'])
def read_receipt(encrypted_invoice_no):
    
    logger.debug('encrypted_invoice_no=%s', encrypted_invoice_no)
    
    if is_not_empty(encrypted_invoice_no):
        
        encrypted_invoice_no = str.encode(encrypted_invoice_no)
        
        #invoice_no  = decrypt(encrypted_invoice_no)
        invoice_no  = encrypted_invoice_no
        receipt_url = None
        request_url = request.url
        
        logger.debug('invoice_no=%s', invoice_no)
        
        db_client = create_db_client(info=current_app.config['database_config'], caller_info=request_url+":read_receipt")
        with db_client.context():
            payment_paid = PaymentPaid.get_by_invoice_no(invoice_no)
            if payment_paid:
                receipt_url = payment_paid.receipt_url
                
        if receipt_url:
            return redirect(receipt_url)
        else:
            abort(400)                
    else:
        abort(400)
        

