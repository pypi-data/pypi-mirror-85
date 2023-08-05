'''
Created on 6 Nov 2020

@author: jacklok
'''

from trexpayment.conf import PAYMENT_GATEWAY_APP_KEY, PAYMENT_GATEWAY_SECRET_KEY, STRIPE_CLIENT_ID
import stripe


stripe_keys = {
  'secret_key'      : PAYMENT_GATEWAY_SECRET_KEY,
  'publishable_key' : PAYMENT_GATEWAY_APP_KEY,
  'client_id'       : STRIPE_CLIENT_ID,
}



def init_stripe():
    
    stripe.api_key          = stripe_keys['secret_key']
    stripe.client_id        = stripe_keys['client_id']
    
    
    return stripe


