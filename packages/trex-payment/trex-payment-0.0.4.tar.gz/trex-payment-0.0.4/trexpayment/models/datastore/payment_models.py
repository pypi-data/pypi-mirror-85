'''
Created on 6 Nov 2020

@author: jacklok
'''
from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexlib.utils.string_util import is_empty, is_not_empty

class PaymentPaid(BaseNModel, DictModel):
    transaction_id          = ndb.StringProperty(required=True)
    invoice_no              = ndb.StringProperty(required=False)
    merchant_acct_key       = ndb.StringProperty(required=True)
    client_reference_no     = ndb.StringProperty(required=False)
    receipt_url             = ndb.StringProperty(required=False)
    transaction_payload     = ndb.JsonProperty(required=True)
    paid_datetime           = ndb.DateTimeProperty(required=True, auto_now_add=True)
    
    @property
    def is_merchant_payment(self):
        return is_empty(self.client_reference_no)
    
    @property
    def is_merchant_customer_payment(self):
        return is_not_empty(self.client_reference_no) and self.merchant_acct_key!=self.client_reference_no
        
    @staticmethod
    def create(transaction_id, merchant_acct_key, transaction_payload, invoice_no=None, receipt_url=None, client_reference_no=None):
        PaymentPaid(transaction_id=transaction_id, 
                    merchant_acct_key=merchant_acct_key, 
                    client_reference_no=client_reference_no, 
                    invoice_no=invoice_no, 
                    receipt_url = receipt_url,
                    transaction_payload=transaction_payload).put()
    
    @staticmethod
    def get_by_invoice_no(invoice_no):
        return PaymentPaid.query(ndb.AND(PaymentPaid.invoice_no==invoice_no)).get()
    

class ChargeSucceeded(BaseNModel, DictModel):
    transaction_id          = ndb.StringProperty(required=True)
    transaction_payload     = ndb.JsonProperty(required=True)
    charged_datetime        = ndb.DateTimeProperty(required=True, auto_now_add=True)
    
    @staticmethod
    def create(transaction_id, transaction_payload):
        ChargeSucceeded(transaction_id=transaction_id, transaction_payload=transaction_payload).put()
        
    
    @staticmethod
    def read(transaction_id):
        return ChargeSucceeded.query(ndb.AND(ChargeSucceeded.transaction_id==transaction_id)).get()
        