'''
Created on 3 Nov 2020

@author: jacklok
'''
from trexlib.utils.crypto_util import encrypt_json, decrypt_json
import base64

def encrypt_payment_details(**params):
    payment_details = {}
    
    payment_details.update(params)
    
    return base64.urlsafe_b64encode(encrypt_json(payment_details))

def decrypt_payment_details(encrypted_payment_details):
    return decrypt_json(base64.urlsafe_b64decode(encrypted_payment_details))