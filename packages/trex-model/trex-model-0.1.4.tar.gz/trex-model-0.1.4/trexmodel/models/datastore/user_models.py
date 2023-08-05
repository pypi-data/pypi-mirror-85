'''
Created on 10 Apr 2020

@author: jacklok
'''
from google.cloud import ndb
from trexmodel.models.datastore.ndb_models import BaseNModel, DictModel
from trexlib.utils.common.cache_util import cache
from flask_login import UserMixin
import logging  
from trexlib.utils.security_util import generate_user_id, hash_password

from trexlib import conf as lib_conf
from trexmodel import conf as model_conf
import json
from json import JSONEncoder

logger = logging.getLogger("ndb_models")

class UserMin(BaseNModel, DictModel, UserMixin):
    
    user_id                     = ndb.StringProperty(required=True)
    password                    = ndb.StringProperty(required=False)
    username                    = ndb.StringProperty(required=False)
    email                       = ndb.StringProperty(required=False)
    gravatar_url                = ndb.StringProperty(required=False)
    #---------------------------------------------------------------------------
    # User Personal Details
    #---------------------------------------------------------------------------
    name                        = ndb.StringProperty(required=False)
    reset_password_reminder     = ndb.BooleanProperty(required=False, default=False)

    last_login_datetime         = ndb.DateTimeProperty(required=False)

    locked                      = ndb.BooleanProperty(required=False, default=False)
    active                      = ndb.BooleanProperty(required=True, default=False)
    try_count                   = ndb.IntegerProperty(required=False)
    
    dict_properties     = ['user_id', 'name', 'email', 'gravatar_url', 'active', 'locked']
    
    @classmethod
    @cache.memoize(timeout=60)
    def get_by_user_id(cls, user_id):
        logger.debug('UserMin.get_by_user_id: read from database')
        return cls.query(cls.user_id==user_id).get()
    
    def get_id(self):
        return self.user_id
    
    @property
    def is_super_user(self):
        return False
    
    @property
    def is_admin_user(self):
        return False
    
    @classmethod
    def create(cls, social_id=None, name=None, email=None,
               gender=None,
               provider=model_conf.APPLICATION_ACCOUNT_PROVIDER, password=None):
        
        user_id = generate_user_id()
        created_user = cls(user_id=user_id, social_id=social_id, name=name, email=email, 
                           gender=gender, provider=provider)
        
        if provider == model_conf.APPLICATION_ACCOUNT_PROVIDER:
            hashed_password = hash_password(user_id, password)
            created_user.password = hashed_password
            
        created_user.put()
        
        return created_user
    
class LoggedInUser(UserMixin):
    
    def __init__(self, json_object, is_super_user=False, is_admin_user=False):
        
        logging.debug('json_object=%s', json_object)
        
        self.user_id            = json_object.get('user_id') 
        self.name               = json_object.get('name')
        self.email              = json_object.get('email')
        self.gravatar_url       = json_object.get('gravatar_url')
        self.active             = json_object.get('active')
        self.locked             = json_object.get('locked')
        self.is_super_user      = is_super_user
        self.is_admin_user      = is_admin_user
        
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return self.self.active
    
    def get_id(self):
        return self.user_id
    
    @property
    def is_anonymous(self):
        return False      

class Role(BaseNModel):
    id              = ndb.StringProperty(required=True)
    name            = ndb.StringProperty(required=True)
    description     = ndb.TextProperty(required=False)


class UserBase(UserMin):
    #---------------------------------------------------------------------------
    # User Personal Details
    #---------------------------------------------------------------------------
    joined_date                 = ndb.DateTimeProperty(required=False, auto_now_add=True)
    bio                         = ndb.TextProperty(required=False, indexed=False)
    birth_date                  = ndb.DateProperty(required=False, indexed=False) 
    gender                      = ndb.StringProperty(required=False, choices=set([model_conf.GENDER_MALE_CODE, model_conf.GENDER_FEMALE_CODE]))
    
    #---------------------------------------------------------------------------
    # Social Media and Open ID Configuration
    #---------------------------------------------------------------------------
    social_id                   = ndb.StringProperty(required=False)
    provider                    = ndb.StringProperty(required=False)
    
    
    @classmethod
    def get_by_social_id(cls, social_id):
        return cls.query(cls.social_id==social_id).get()
    
    dict_properties = ['name', 'provider', 'username', 'email', 'birth_date']


    @property
    def gender_label(self):
        if model_conf.GENDER_MALE_CODE == self.gender:
            return 'Male'
        elif model_conf.GENDER_FEMALE_CODE == self.gender:
            return 'Female'
        else:
            return 'Unknown'

    @property
    def age(self):
        if self.birth_date:
            from dateutil.relativedelta import relativedelta
            from datetime import date
            today   = date.today()
            __age   = relativedelta(today, self.birth_date)
            return __age.years
        else:
            return 0

class User(UserBase):

    #---------------------------------------------------------------------------
    # User Contact Details
    #---------------------------------------------------------------------------
    country                     = ndb.StringProperty(required=False, default=lib_conf.DEFAULT_COUNTRY_CODE)
    state                       = ndb.StringProperty(required=False)
    city                        = ndb.StringProperty(required=False, )
    postcode                    = ndb.StringProperty(required=False, )
    address                     = ndb.StringProperty(required=False, )
    house_phone                 = ndb.StringProperty(required=False, )
    office_phone                = ndb.StringProperty(required=False, )
    mobile_phone                = ndb.StringProperty(required=False, )
    national_id                 = ndb.StringProperty(required=False, )
    auth_token                  = ndb.StringProperty(required=False, )
    
    is_email_verified           = ndb.BooleanProperty(required=False, default=False)
    is_mobile_phone_verified    = ndb.BooleanProperty(required=False, default=False)

    modified_datetime           = ndb.DateTimeProperty(required=True, auto_now=True)
    
    
    dict_properties = ['name', 'username', 'email', 'birth_date', 'reference_code']

    #unique_attributes = 'email,username'

    audit_properties            = [
                                    'username', 'email', 'password', 'name', 'birth_date', 'gender','reference_code_value',
                                    'country', 'state', 'city', 'postcode', 'address', 'house_phone', 'office_phone', 'mobile_phone', 'redeem_pin', 'required_redeem_pin_verification',

                                    ]

    unicode_properties = ['name', 'address', 'city']

    export_properties = (
        ('User Id','user_id'),
        ('Name','name'),
        ('Username','username'),
        ('Reference Code','reference_code_value'),
        ('Email','email'),
        ('Gender','gender'),
        ('Date of Birth','birth_date'),
        ('Country','country_desc'),
        ('State','state_desc'),
        ('City','city'),
        ('Address','address'),
        ('House Phone','house_phone'),
        ('Office Phone','office_phone'),
        ('Mobile Phone','mobile_phone'),
        ('Joined Date','joined_date'),

    )

    def __repr__(self):
        return '''
                User[key=%s, 
                user_id=%s, 
                username=%s, 
                name=%s, 
                email=%s, 
                mobile_phone=%s, 
                provider=%s, 
                country=%s, 
                locked=%s,
                active=%s
                ]
                ''' % (self.key_in_str, self.user_id, self.username, self.name, self.email, self.mobile_phone, self.provider, self.country, self.locked, self.active)

    @classmethod
    def get_by_email(cls, email, provider=model_conf.APPLICATION_ACCOUNT_PROVIDER):
        result =  User.query(ndb.AND(User.email==email, User.provider==provider)).fetch(limit=1)
        if result:
            return result[0]
        
    @classmethod
    def get_by_auth_token(cls, auth_token):
        result =  User.query(ndb.AND(User.auth_token==auth_token)).fetch(limit=1)
        if result:
            return result[0]    
    
    @property
    def is_active(self):
        """Returns `True` if the user is active."""
        logger.info('calling is_active')
        #return self.active
        return True

    def get_auth_token(self):
        logger.info('calling get_auth_token')
        return self.auth_token

    def has_role(self, role):
        """Returns `True` if the user identifies with the specified role.

        :param role: A role name or `Role` instance"""
        if isinstance(role, str):
            return role in (role.name for role in self.roles)
        else:
            return role in self.roles

    def get_security_payload(self):
        logger.info('calling get_security_payload')
        """Serialize user object as response payload."""
        return {'id': str(self.id)}

    def to_simple_json(self):
        birth_date_str = None
        if self.birth_date:
            birth_date_str = self.birth_date.strftime('%d/%m/%Y')


        user_detail_in_json = {
            "reference_code"                    : self.reference_code,
            "name"                              : self.name,
            "email"                             : self.email,
            "username"                          : self.username,
            "birth_date"                        : birth_date_str,
            "mobile_phone"                      : self.mobile_phone,
            "gender"                            : self.gender,
            "provider"                          : self.provider,
            "user_id"                           : self.key_in_str,
            "address"                           : self.address,
            "postcode"                          : self.postcode,
            "city"                              : self.city,
            "state"                             : self.state,
            "country"                           : self.country,
            "mobile_phone"                      : self.mobile_phone,
            "office_phone"                      : self.office_phone,
            "house_phone"                       : self.house_phone,
            "active"                            : self.active,
            

        }
        logging.debug(user_detail_in_json)
        return user_detail_in_json    


    
