'''
Created on 3 Nov 2020

@author: jacklok
'''
import unittest
from trexpayment.util.payment_util import encrypt_payment_details, decrypt_payment_details

class TestPaymentUtil(unittest.TestCase):


    def test_create_encrypted_payment_details(self):
        sku = '100'
        amount = 100
        desc = 'bla bla'
        invoice_no = '101010'
        something = 'something'
        encrypted_payment_details = encrypt_payment_details(sku=sku, amount=amount, desc=desc, invoice_no=invoice_no, something=something)
        
        assert encrypted_payment_details is not None
        
        
        decrypted_payment_details = decrypt_payment_details(encrypted_payment_details)
        
        assert decrypted_payment_details is not None
        assert decrypted_payment_details.get('amount') == amount
        assert decrypted_payment_details.get('sku') == sku
        assert decrypted_payment_details.get('desc') == desc
        assert decrypted_payment_details.get('invoice_no') == invoice_no
        assert decrypted_payment_details.get('something') == something


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()