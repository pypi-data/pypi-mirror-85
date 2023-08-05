'''
Created on 4 Nov 2020

@author: jacklok
'''

import logging, os

APPLICATION_NAME                            = 'Trex-Payment'
APPLICATION_TITLE                           = 'Trex Payment Gateway'
APPLICATION_DESC                            = 'Trex payment gateway for service payment'
APPLICATION_HREF                            = 'http://localhost.com:8082/'

PRODUCTION_MODE                             = "PROD"
DEMO_MODE                                   = "DEMO"
LOCAL_MODE                                  = "LOCAL"


#DEPLOYMENT_MODE                             = PRODUCTION_MODE
DEPLOYMENT_MODE                             = DEMO_MODE
#DEPLOYMENT_MODE                             = LOCAL_MODE

PAYMENT_GATEWAY_APP_KEY                     = ''
PAYMENT_GATEWAY_SECRET_KEY                  = ''

STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_LIVE     = os.environ.get('STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_LIVE')
STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_LIVE  = os.environ.get('STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_LIVE')

STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_TEST     = os.environ.get('STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_TEST')
STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_TEST  = os.environ.get('STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_TEST')

APP_LOGO_PATH                               = os.environ.get('APP_LOGO_PATH') 
APP_LOADING_PATH                            = os.environ.get('APP_LOADING_PATH') 


CSRF_ENABLED                                        = True

CONTENT_WITH_JAVASCRIPT_LINK                        = True

SUPPORTED_LANGUAGE                                  = ["en"]
 
APPLICATION_VERSION_NO                              = "04102020"


SUPERUSER_ID                                        = os.environ.get('SUPERUSER_ID')
SUPERUSER_EMAIL                                     = os.environ.get('SUPERUSER_EMAIL')
SUPERUSER_HASHED_PASSWORD                           = os.environ.get('SUPERUSER_HASHED_PASSWORD')

STRIPE_CONNECT_ONBOARD_URL                          = ''
STRIPE_CONNECT_ONBOARD_REFRESH_URL                  = ''
STRIPE_CONNECT_ONBOARD_RETURN_URL                   = ''

STRIPE_CLIENT_ID                                    = ''


PAYMENT_SUCCESS_URL                                 = ''
PAYMENT_CANCEL_URL                                  = ''

SUPPORT_EMAIL                                       = 'support@penefit.com'

if DEPLOYMENT_MODE==PRODUCTION_MODE:
    DEBUG_MODE       = False
    #DEBUG_MODE       = True

    #LOGGING_LEVEL    = logging.DEBUG
    #LOGGING_LEVEL    = logging.WARN
    LOGGING_LEVEL    = logging.INFO
    #LOGGING_LEVEL    = logging.ERROR
    
    PAYMENT_GATEWAY_APP_KEY                 = STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_LIVE
    PAYMENT_GATEWAY_SECRET_KEY              = STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_LIVE
    
    STRIPE_CONNECT_ONBOARD_URL                          = 'https://payment.penefit.com/integrate/onboard-user'
    STRIPE_CONNECT_ONBOARD_REFRESH_URL                  = 'https://payment.penefit.com/integrate/onboard-user/refresh'
    STRIPE_CONNECT_ONBOARD_RETURN_URL                   = 'https://payment.penefit.com/integrate/onboard-user/return'
    
    PAYMENT_SUCCESS_URL                                 = 'https://payment.penefit.com/checkout/payment-success?session_id={CHECKOUT_SESSION_ID}'
    PAYMENT_CANCEL_URL                                  = 'https://payment.penefit.com/checkout/payment-cancel'
    
    STRIPE_CLIENT_ID                                    = 'ca_IK1991GJpxfZPNHXPdfmsU49dvf3OZNq'

    
    
elif DEPLOYMENT_MODE==DEMO_MODE:
    DEBUG_MODE       = True
    #DEBUG_MODE       = False
    
    LOGGING_LEVEL    = logging.DEBUG
    #LOGGING_LEVEL    = logging.INFO
    
    PAYMENT_GATEWAY_APP_KEY                 = STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_TEST
    PAYMENT_GATEWAY_SECRET_KEY              = STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_TEST
    
    STRIPE_CONNECT_ONBOARD_URL                          = 'https://payment-dev.penefit.com/integrate/onboard-user'
    STRIPE_CONNECT_ONBOARD_REFRESH_URL                  = 'https://payment-dev.penefit.com/integrate/onboard-user/refresh'
    STRIPE_CONNECT_ONBOARD_RETURN_URL                   = 'https://payment-dev.penefit.com/integrate/onboard-user/return'
    
    
    #PAYMENT_SUCCESS_URL                                 = 'https://ca86e5e356e0.ngrok.io/checkout/payment-success?session_id={CHECKOUT_SESSION_ID}'
    #PAYMENT_CANCEL_URL                                  = 'https://ca86e5e356e0.ngrok.io/checkout/payment-cancel'
    
    PAYMENT_SUCCESS_URL                                 = 'https://payment-dev.penefit.com/checkout/payment-success?session_id={CHECKOUT_SESSION_ID}'
    PAYMENT_CANCEL_URL                                  = 'https://payment-dev.penefit.com/checkout/payment-cancel'
    
    STRIPE_CLIENT_ID                                    = 'ca_IK19spOpFM1kcUMqGPq8jM5MyQ1ENpqa'

    APP_LOGO_PATH                                       = os.environ.get('APP_DEV_LOGO_PATH')

elif DEPLOYMENT_MODE==LOCAL_MODE:
    DEBUG_MODE       = True

    LOGGING_LEVEL    = logging.DEBUG
    #LOGGING_LEVEL    = logging.INFO
    
    PAYMENT_GATEWAY_APP_KEY                 = STRIPE_PAYMENT_GATEWAY_APP_KEY_FOR_TEST
    PAYMENT_GATEWAY_SECRET_KEY              = STRIPE_PAYMENT_GATEWAY_SECRET_KEY_FOR_TEST
    
    PAYMENT_SUCCESS_URL                                 = 'https://ca86e5e356e0.ngrok.io/checkout/payment-success?session_id={CHECKOUT_SESSION_ID}'
    PAYMENT_CANCEL_URL                                  = 'https://ca86e5e356e0.ngrok.io/checkout/payment-cancel'


SUPPORT_LANGUAGES                               = ['en','zh']

#-----------------------------------------------------------------
# Web Beacon settings
#-----------------------------------------------------------------
WEB_BEACON_TRACK_EMAIL_OPEN   = 'eo'

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "json": {
            "()": "flask_google_cloud_logger.FlaskGoogleCloudFormatter",
            "application_info": {
                "type": "python-application",
                "application_name": "Penefit Payment"
            },
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        }
    },
    "handlers": {
        "json": {
            "class": "logging.StreamHandler",
            "formatter": "json"
        }
    },
    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["json"]
        },
        #"werkzeug": {
        #    "level": "WARN",  # Disable werkzeug hardcoded logger
        #    "handlers": ["json"]
        #}
    }
}


STRIPE_WEBHOOK_EVENT_TYPE_SECRET_MAPPING = {
                                            'payout.paid': 'whsec_xZkksxl2ybQd0ocycrhjiTfzVuRbxaWM',
                                            'charge.succeeded': 'whsec_JOaYYZfUwfCwuXVt2doC3efUAHHWOwYJ',
                                            'checkout.session.async_payment_succeeded': 'whsec_aBWrcvZ9MRpasTYwxmtQorw8nupj3VAT',
                                            }



