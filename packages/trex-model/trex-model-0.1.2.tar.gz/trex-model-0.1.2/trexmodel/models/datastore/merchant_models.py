'''
Created on 15 May 2020

@author: jacklok
'''

from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel, FullTextSearchable
from trexmodel.models.datastore.system_models import SentEmail
from trexlib.utils.string_util import random_number
import logging

class MerchantMin(BaseNModel, DictModel, FullTextSearchable):
    
    company_name            = ndb.StringProperty(required=True)
    contact_name            = ndb.StringProperty(required=False)
    address                 = ndb.StringProperty(required=False)
    office_phone            = ndb.StringProperty(required=False)
    mobile_phone            = ndb.StringProperty(required=False)
    fax_phone               = ndb.StringProperty(required=False)
    email                   = ndb.StringProperty(required=False)
    status                  = ndb.StringProperty(required=False)
    account_code            = ndb.StringProperty(required=False)
    modified_datetime       = ndb.DateTimeProperty(required=True, auto_now=True)
    registered_datetime     = ndb.DateTimeProperty(required=True, auto_now_add=True)
    plan_start_date         = ndb.DateProperty(required=True)
    plan_end_date           = ndb.DateProperty(required=True)
    
    searchable_field_name   = 'company_name'
    
    dict_properties = ['company_name', 'contact_name', 'mobile_phone', 'email', 'account_code', 
                       'registered_datetime', 'modified_datetime', 'plan_start_date', 'plan_end_date']

class MerchantAcct(MerchantMin):
    
    
    @staticmethod
    def create(company_name=None, contact_name=None, email=None, mobile_phone=None, office_phone=None, plan_start_date=None, plan_end_date=None, account_code=None):
        
        if account_code is None:
            account_code    = "%s-%s-%s-%s" % (random_number(4),random_number(4),random_number(4),random_number(4))
            
        merchant_acct   = MerchantAcct(company_name=company_name, 
                                       contact_name = contact_name,
                                       email = email,
                                       mobile_phone = mobile_phone,
                                       office_phone = office_phone,
                                       plan_start_date=plan_start_date, 
                                       plan_end_date=plan_end_date)
        
        logging.debug('account_code=%s', account_code)
        
        merchant_acct.account_code = account_code
        
        merchant_acct.put()
        
        return merchant_acct
    
    @staticmethod
    def get_by_account_code(account_code):
        return MerchantAcct.query(ndb.AND(MerchantAcct.account_code==account_code)).get()
        
    
    @staticmethod
    def list(offset=0, limit=10):
        return MerchantAcct.query().order(-MerchantAcct.registered_datetime).fetch(offset=offset, limit=limit)
    
class MerchantSentEmail(SentEmail):
    '''
    Merchant account as Ancestor
    '''
    pass    
    
    