'''
Created on 15 Apr 2020

@author: jacklok
'''
from google.cloud import ndb
from google.oauth2 import service_account
from google.auth import crypt
import io, json, logging
from trexmodel import conf as model_conf
import six

logger = logging.getLogger('root')

def create_db_client(info=None, credential_filepath=None, namespace=None, caller_info=None):
    
    #datastore_cred = service_account.Credentials.from_service_account_file(lib_conf.DATASTORE_CREDENTIAL_PATH)
    logger.debug('create_db_client: caller_info=%s', caller_info)
    #logger.debug('create_db_client: info=%s', info)
    if info:
        datastore_cred = service_account.Credentials.from_service_account_info(info)
    else: 
        if credential_filepath:
            datastore_cred = service_account.Credentials.from_service_account_file(credential_filepath)
        else:
            datastore_cred = service_account.Credentials.from_service_account_file(
                                                            model_conf.DATASTORE_CREDENTIAL_PATH)
            
    client = ndb.Client(credentials=datastore_cred, project=model_conf.MODEL_PROJECT_ID, namespace=namespace)
    
    return client


def from_dict(data, require=None):
    
    keys_needed = set(require if require is not None else [])

    missing = keys_needed.difference(six.iterkeys(data))

    if missing:
        raise ValueError(
            "Service account info was not in the expected format, missing "
            "fields {}.".format(", ".join(missing))
        )

    # Create a signer.
    signer = crypt.RSASigner.from_service_account_info(data)

    return signer

def read_service_account_file(credential_filepath=model_conf.DATASTORE_CREDENTIAL_PATH):
    with io.open(credential_filepath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data, from_dict(data)
    
    

