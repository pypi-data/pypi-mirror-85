'''
Created on 6 Nov 2020

@author: jacklok
'''
from trexpayment.conf import STRIPE_WEBHOOK_EVENT_TYPE_SECRET_MAPPING
from trexpayment.util.stripe_helpers import init_stripe
from trexlib.utils.log_util import get_tracelog
from functools import wraps
from flask import abort, request
import logging as logger, stripe
from datetime import datetime

#logger = logging.getLogger('root')

TRANSACTION_ALLOW_FOR_DELAY_IN_SECOND = 5*60

def __get_payload_and_signature():
    payload = request.data.decode("utf-8")
    
    received_sig = request.headers.get("Stripe-Signature", None)
    
    return (payload, received_sig)


def __get_end_point_secret(webhook_event_mapping):
    endpoint_secret = STRIPE_WEBHOOK_EVENT_TYPE_SECRET_MAPPING.get(webhook_event_mapping)
    return endpoint_secret

def stripe_webhook_event_secret_verify(webhook_event_mapping):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            
            (payload, received_sig) = __get_payload_and_signature()
             
            logger.debug('stripe_webhook_endpoint_verify(%s): payload=%s', webhook_event_mapping, payload)
            logger.debug('stripe_webhook_endpoint_verify(%s): received_sig=%s', webhook_event_mapping, received_sig)
            
            endpoint_secret = __get_end_point_secret(webhook_event_mapping)
            
            logger.debug('stripe_webhook_endpoint_verify(%s): payload=%s', webhook_event_mapping, endpoint_secret)
            
            if endpoint_secret:
        
                try:
                    
                    received_sig_arrays = received_sig.split(',')
            
                    event_timestamp_value   = received_sig_arrays[0].split('=')[1]
                    
                    logger.debug('stripe_webhook_endpoint_verify(%s): event_timestamp_value=%s', webhook_event_mapping, event_timestamp_value)
                    
                    event_datetime          = datetime.fromtimestamp(int(event_timestamp_value))
                    
                    now                     = datetime.now()
                    
                    time_differene = now - event_datetime
                    
                    logger.debug('stripe_webhook_endpoint_verify(%s): event_datetime=%s', webhook_event_mapping, event_datetime)
                    logger.debug('stripe_webhook_endpoint_verify(%s): now=%s', webhook_event_mapping, now)
                    logger.debug('stripe_webhook_endpoint_verify(%s): time_differene=%s', webhook_event_mapping, time_differene)
                    
                    if time_differene.seconds > TRANSACTION_ALLOW_FOR_DELAY_IN_SECOND:
                        logger.warn('Delay transaction, could be replay attack!')
                        abort(400)
                        
                    stripe  = init_stripe()
                    event   = stripe.Webhook.construct_event(
                                        payload, received_sig, endpoint_secret
                                    )
                    
                    logger.debug('stripe_webhook_endpoint_verify(%s): event=%s', webhook_event_mapping, event)
                    
                    if event:
                        return f(*args, **kwargs)
                    else:
                        abort(400)
                
                except ValueError:
                    abort(400)
                except stripe.error.SignatureVerificationError:
                    abort(400)
                except:
                    
                    get_tracelog()
                    abort(400)        
            else:
                abort(403)
            
        return wrapper
    return decorator


