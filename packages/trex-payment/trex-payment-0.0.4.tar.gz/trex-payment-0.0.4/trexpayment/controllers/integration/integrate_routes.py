'''
Created on 17 Sep 2020

@author: jacklok
'''
from trexpayment.conf import PAYMENT_GATEWAY_APP_KEY, PAYMENT_GATEWAY_SECRET_KEY,\
    STRIPE_CLIENT_ID, STRIPE_CONNECT_ONBOARD_REFRESH_URL, STRIPE_CONNECT_ONBOARD_RETURN_URL, STRIPE_CONNECT_ONBOARD_URL
from flask import Blueprint, render_template, session, abort, redirect, jsonify, request, Response
from flask.helpers import url_for
import stripe
import logging, jinja2



stripe_keys = {
  'secret_key'      : PAYMENT_GATEWAY_SECRET_KEY,
  'publishable_key' : PAYMENT_GATEWAY_APP_KEY,
  'client_id'       : STRIPE_CLIENT_ID,
}

stripe.api_key          = stripe_keys['secret_key']
stripe.client_id        = stripe_keys['client_id']


STRIPE_PUBLISHABLE_KEY = PAYMENT_GATEWAY_APP_KEY


integrate_bp = Blueprint('integrate_bp', __name__,
                     template_folder='templates',
                     static_folder='static',
                     url_prefix='/integrate')


@integrate_bp.route("/authorize")
def authorize():
    scope   = request.args.get("scope")
    
    url     = stripe.OAuth.authorize_url(scope=scope, redirect_uri=STRIPE_CONNECT_ONBOARD_URL)
    return redirect(url)


@integrate_bp.route("/oauth/callback")
def callback():
    code    = request.args.get("code")
    
    try:
        resp = stripe.OAuth.token(grant_type="authorization_code", code=code)
    except stripe.oauth_error.OAuthError as e:
        return "Error: " + str(e)

    return """
<p>Success! Account <code>{stripe_user_id}</code> is connected.</p>
<p>Click <a href="/deauthorize?stripe_user_id={stripe_user_id}">here</a> to
disconnect the account.</p>
""".format(
        stripe_user_id=resp["stripe_user_id"]
    )


@integrate_bp.route("/deauthorize")
def deauthorize():
    stripe_user_id = request.args.get("stripe_user_id")
    try:
        stripe.OAuth.deauthorize(stripe_user_id=stripe_user_id)
    except stripe.oauth_error.OAuthError as e:
        return "Error: " + str(e)

    return """
<p>Success! Account <code>{stripe_user_id}</code> is disconnected.</p>
<p>Click <a href="/">here</a> to restart the OAuth flow.</p>
""".format(
        stripe_user_id=stripe_user_id
    )


def _generate_account_link(account_id):
    account_link = stripe.AccountLink.create(
                            type            = 'account_onboarding',
                            account         = account_id,
                            refresh_url     = STRIPE_CONNECT_ONBOARD_REFRESH_URL,
                            return_url      = STRIPE_CONNECT_ONBOARD_RETURN_URL,
                    )
    return account_link.url

@integrate_bp.route('/onboard-user', methods=['POST','GET'])
def account_onboarding(): 
    
    account = stripe.Account.create(type='standard')
    # Store the account ID.
    session['account_id']   = account.id

    account_link_url        = _generate_account_link(account.id)
    
    logging.debug('account_onboarding: account_link_url=%s', account_link_url)
    
    try:
        return redirect(account_link_url)
    except Exception as e:
        return jsonify(error=str(e)), 403


@integrate_bp.route('/onboard-user/refresh', methods=['GET'])
def account_onboard_refresh(): 
    
    if 'account_id' not in session:
        return redirect('/')

    account_id = session['account_id']

    account_link_url = _generate_account_link(account_id)
    
    logging.debug('account_onboard_refresh: account_link_url=%s', account_link_url)
    
    return redirect(account_link_url)


@integrate_bp.route('/onboard-user/return', methods=['GET'])
def account_onboard_return(): 
    
    return render_template("integration/you_have_onboard.html", 
                           home_page_url = url_for('main_bp.home_page')
                           )
    
    
 


           
    
