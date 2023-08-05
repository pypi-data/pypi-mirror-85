'''
Created on 8 May 2020

@author: jacklok
'''
from google.cloud import ndb
from trexmodel.models.datastore.user_models import UserMin
from trexlib.utils.security_util import generate_user_id, hash_password


class SuperUser(UserMin):
    created_datetime                 = ndb.DateTimeProperty(required=False, auto_now_add=True)
    
    dict_properties = ['user_id', 'name', 'email', 'gravatar_url', 'active', 'locked']
    
    @property
    def is_super_user(self):
        return True
    
    @property
    def is_admin_user(self):
        return False
    
    @classmethod
    def new_super_user_id(cls):
        return 'superuser'
    
    @classmethod
    def create(cls, name=None, email=None, password=None, active=False):
        
        user_id = cls.new_super_user_id()
        created_user = cls(user_id=user_id, name=name, email=email, active=active)
        
        hashed_password         = hash_password(user_id, password)
        created_user.password   = hashed_password
            
        created_user.put()
        return created_user
    
    @staticmethod
    def list(offset=0, limit=10):
        return AdminUser.query().order(-AdminUser.joined_date).fetch(offset=offset, limit=limit)
    
    @staticmethod
    def get_by_email(email):
        return AdminUser.query(ndb.AND(AdminUser.email==email)).get()
    
class AdminUser(SuperUser):
    
    dict_properties = ['user_id', 'name', 'email', 'gravatar_url', 'active', 'locked', 'created_datetime']
    
    @classmethod
    def new_super_user_id(cls):
        return generate_user_id()
    
    @property
    def is_super_user(self):
        return False
    
    @property
    def is_admin_user(self):
        return True
    

