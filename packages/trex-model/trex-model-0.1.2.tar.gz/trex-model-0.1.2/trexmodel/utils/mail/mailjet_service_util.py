'''
Created on 9 Jun 2020

@author: jacklok
'''
#from models.datastore.merchant_models import MerchantSentEmail
from trex.utils.string_util import random_string
from trex.utils.mail.mailjet_util import send_email
from six import string_types
import logging, json
from trex.conf import lib_conf
'''
def send_merchant_email_by_batch(subject=None, sender=None, merchant_acct=None, html=None, body=None, to_address=None, cc_address=None, bcc_addres=None, batch_id=None):
    if merchant_acct is None:
        raise Exception('Missing merchant account')
    else:
        if batch_id is None:
            batch_id = random_string(12)
        
        sent_address = []
        if isinstance(to_address, string_types):
            sent_address.append(to_address)
        elif isinstance(to_address, (tuple, list)):
            sent_address = to_address
        
        logging.debug('Going to create MerchantSentEmail with sent_address=%s', sent_address)
            
        #send email here
        response = send_email(sender=sender, to_address=to_address, cc_address=cc_address, bcc_address=bcc_addres, subject=subject, 
                                body=body, html=html, batch_id=batch_id)
        
        logging.debug('Sent email response=%s', response)
        
        for s in sent_address:
            sent_response = response.get(s)
            logging.debug('sent_response=%s', sent_response)
            MerchantSentEmail(
                            parent          = merchant_acct.create_ndb_key(),
                            email_id        = str(sent_response.get('message_id')),
                            batch_id        = batch_id,
                            to              = s,
                            subject         = subject,
                            html            = html,
                            body            = body,
                            sent_response   = json.dumps(sent_response),
                            ).put()
'''                            
def send_single_email(subject=None, sender=lib_conf.DEFAULT_SENDER, html=None, body=None, to_address=None, cc_address=None, bcc_addres=None):
    response = send_email(sender        = sender, 
                          to_address    = to_address,  
                          cc_address    = cc_address, 
                          bcc_address   = bcc_addres, 
                          subject       = subject, 
                          body          = body, 
                          html          = html
                          )
        
    logging.debug('Sent email response=%s', response)                       
        
    
    
    