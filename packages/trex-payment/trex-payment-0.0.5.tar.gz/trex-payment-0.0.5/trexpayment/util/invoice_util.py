'''
Created on 9 Nov 2020

@author: jacklok
'''

from datetime import datetime
from trexlib.utils.common.common_util import id_generator
import string

def generate_invoice_no():
    today = datetime.now().date()
    
    date_str = today.strftime('%Y%m%d')
    
    return '%s-%s' % (date_str, id_generator(size=8, chars=string.digits)) 
