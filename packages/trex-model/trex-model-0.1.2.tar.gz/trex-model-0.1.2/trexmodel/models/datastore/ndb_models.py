'''
Created on 13 Apr 2020

@author: jacklok
'''
from google.cloud import ndb
from trexlib.utils.common.float_util import format_float
from datetime import datetime, date, time
from trexlib.utils.string_util import is_not_empty 
from trexlib.utils.log_util import get_tracelog
from six import string_types 
from trexlib.utils.common.date_util import increase_date 
import logging
from google.cloud.ndb._datastore_query import Cursor
from trexlib import conf as lib_conf 
from trexmodel import conf as model_conf
 
logging = logging.getLogger('application:ndb_models') 

def convert_to_serializable_value(val, none_as_empty_string=False, gmt=0, 
                                  datetime_format=lib_conf.DEFAULT_DATETIME_FORMAT, 
                                  date_format=lib_conf.DEFAULT_DATE_FORMAT, 
                                  time_format=lib_conf.DEFAULT_TIME_FORMAT):
    if isinstance(val, (list, tuple)):
        _list = []
        for item in val:
            _list.append(convert_to_serializable_value(item))
        value = _list
    elif isinstance(val, float):
        value = format_float(val)
    elif isinstance(val, (dict, int, bool)):
        #logging.debug('>>>>found dict, int, float, bool value=%s', val)
        value = val
    elif isinstance(val, datetime):
        gmt_datetime = increase_date(val, hour=gmt)
        value = gmt_datetime.strftime(datetime_format)
    elif isinstance(val, date):
        value = val.strftime(date_format)
    elif isinstance(val, time):
        #gmt_datetime = increase_date(val, hours=gmt)
        value = val.strftime(time_format)
    else:
        if none_as_empty_string:
            if val:
                value = str(val)
            else:
                value = ''
        else:
            if val is None:
                value = None
            else:
                value = str(val)
    #logging.debug('convert_to_serializable_value: value=%s', value)
    return value

def render_dict_value(val, full=False, show_key=True, gmt=0, 
                      datetime_format=lib_conf.DEFAULT_DATETIME_FORMAT, 
                      date_format=lib_conf.DEFAULT_DATE_FORMAT, 
                      time_format=lib_conf.DEFAULT_TIME_FORMAT):
    #logging.debug('---render_dict_value---')
    value = None
    if isinstance(val, DictModel):
        value = val.to_dict(full=full, show_key=show_key, gmt=gmt, datetime_format=datetime_format, date_format=datetime_format, time_format=time_format)

    elif isinstance(val, ndb.Model):
        value = val.key.urlsafe()

    elif isinstance(val, (list, tuple)):
        _list = []
        for item in val:
            _list.append(render_dict_value(item, full=full, show_key=show_key, gmt=gmt, datetime_format=datetime_format, date_format=datetime_format, time_format=time_format))
        value = _list

    elif isinstance(val, DictObject):
        value = val.to_dict(gmt=gmt)
    else:
        value = convert_to_serializable_value(val, gmt=gmt, datetime_format=datetime_format, date_format=datetime_format, time_format=time_format)
    return value

class DictObject(object):
    dict_properties = None
    
    def get_class_members(self, klass):
        ret = dir(klass)
        if hasattr(klass,'__bases__'):
            for base in klass.__bases__:
                ret = ret + self.get_class_members(base)
        return ret
    
    def uniq(self, seq ): 
        return list(set(seq))
    
    def properties(self):
        return self.__dict__

    def to_dict(self, full=True, show_key=True, dict_properties=None, gmt=lib_conf.DEFAULT_GMT, 
                        datetime_format=lib_conf.DEFAULT_DATETIME_FORMAT, 
                        date_format=lib_conf.DEFAULT_DATE_FORMAT, 
                        time_format=lib_conf.DEFAULT_TIME_FORMAT):
        logging.info('calling DictObject.to_dict')
        result = {}
        #logging.debug('properties = %s, object = %s', self.properties(), self)

        _dict_properties = dict_properties or self.dict_properties

        if _dict_properties:
            for p in _dict_properties:

                val = getattr(self, p)
                if val is not None:
                    #logging.debug('attribute=%s', p)
                    result[p] = render_dict_value(val, full=full, show_key=show_key, gmt=gmt, 
                                                  datetime_format=datetime_format, 
                                                  date_format=datetime_format, 
                                                  time_format=time_format)
        return result
    
class DictModel(ndb.Model):
    
    dict_properties             = None
    dict_full_properties        = None
    show_key_in_dict            = True

    def __get_attr_value(self, obj, attr_name):
        val = getattr(obj, attr_name)
        return val

    def put(self, **kwargs):
        super(DictModel, self).put(**kwargs)

    def to_dict(self, full=False, show_key=True, dict_properties=None, gmt=lib_conf.DEFAULT_GMT, 
                        datetime_format=lib_conf.DEFAULT_DATETIME_FORMAT, 
                        date_format=lib_conf.DEFAULT_DATE_FORMAT, 
                        time_format=lib_conf.DEFAULT_TIME_FORMAT):
        result = {}
        logging.debug('DictModel: full=%s', full)
        logging.debug('DictModel: show_key=%s', show_key)
        
        if self.show_key_in_dict or show_key:
            result['key'] = self.key.urlsafe().decode("utf-8") 
        
        _dict_properties = dict_properties or self.dict_properties

        if full and self.dict_full_properties:
            _dict_properties = self.dict_full_properties

        if _dict_properties:
            for p in _dict_properties:
                if p=='key':
                    if result.get('key'):
                        continue
                    
                _p = p.split('.')

                if len(_p)>1:
                    ref_array   = _p[:-1]
                    ref_obj     = self
                    for _a in ref_array:
                        ref_obj = self.__get_attr_value(ref_obj, _a)

                    if ref_obj:
                        ref_value = self.__get_attr_value(ref_obj, _p[-1])
                else:
                    ref_value = self.__get_attr_value(self, p)

                if is_not_empty(ref_value):
                #if ref_value:
                    p = p.replace('.', '_')
                    result[p] = render_dict_value(ref_value, full=full, show_key=show_key, gmt=gmt, datetime_format=datetime_format, date_format=datetime_format, time_format=time_format)
                                        
        #logging.debug('DictModel: result=%s', result)
        
        return result    

class NDBModel(object):
    @classmethod
    def get_by_ndb_id(cls, ndb_id):
        if isinstance(ndb_id, string_types):
            return cls.get_by_key_name(ndb_id)
        else:
            return cls.get_by_id(ndb_id)

    def ndb_id(self):
        return self.key().id()

    def create_ndb_key(self):
        return ndb.Key(flat=self.key.flat())
    
class BaseNModel(DictModel, NDBModel):

    saved = False

    def is_saved(self):
        return self.saved

    @classmethod
    def _post_get_hook(cls, key, future):
        obj = future.get_result()
        if obj is not None:
            # test needed because post_get_hook is called even if get() fails!
            obj.saved = True

    def _post_put_hook(self, future):
        self.saved = True

    @property
    def key_in_str(self):
        return self.key.urlsafe().decode('utf-8')

    @property
    def key_name(self):
        return self.key.id()

    def equal(self, another_instance):
        if another_instance:
            return self.key_in_str == another_instance.key_in_str
        else:
            return False

    def not_equal(self, another_instance):
        if another_instance:
            return self.key_in_str != another_instance.key_in_str
        else:
            return True
        
    
    @classmethod
    def fetch(cls, model_key):
        try:
            if model_key:
                return ndb.Key(urlsafe=model_key).get()

        except:
            logging.error('Failed to fetch entity due to %s', get_tracelog())

        return None
    
    @classmethod
    def count(cls, limit=model_conf.MAX_FETCH_RECORD): 
        
        query = cls.query()
        
        return query.count(limit=limit, keys_only=True)
            
    @classmethod
    def list_all(cls, offset=0,  start_cursor=None, return_with_cursor=False, keys_only=False, 
                 limit=model_conf.PAGINATION_SIZE):
        
        query = cls.query()
        
        if start_cursor or return_with_cursor:
            #if start_cursor is None:
            #    start_cursor = ''
            
            (search_results, next_cursor, more)       = query.fetch_page(page_size=limit, start_cursor=start_cursor, keys_only=keys_only)
            logging.debug('##########################################')
            
            logging.debug('list_all: search_results=%s', search_results)
            logging.debug('list_all: next_cursor=%s', next_cursor)
            logging.debug('list_all: more=%s', more) 
            
            logging.debug('##########################################')
            
            if more:
                return search_results, next_cursor.to_websafe_string().decode('utf-8')  
            else:    
                return search_results, 'None'
            
        else:
            search_results = query.fetch(limit=limit, offset=offset)
            
            return search_results
    
    
class FullTextSearchable(ndb.Model):
    full_text_search_field = ndb.StringProperty(repeated=True)
    
    searchable_field_name = None
    
    def _pre_put_hook(self):
        """before save, parse searchable field into strings"""
        _searchable_field_name = self.searchable_field_name
        logging.debug('_searchable_field_name=%s', _searchable_field_name)
        if _searchable_field_name:
            searchable_field_value = getattr(self, _searchable_field_name)
            logging.debug('searchable_field_value=%s', searchable_field_value)
            if is_not_empty(searchable_field_value):
                splitted_words = searchable_field_value.lower().split(' ')
                
                logging.debug('splitted_words=%s', splitted_words)
                
                searchable_words_list = [x for x in splitted_words if x and len(x) > 2]
                logging.debug('searchable_words_list=%s', searchable_words_list)
                
                self.full_text_search_field = searchable_words_list
    
    
    
    @classmethod
    def full_text_count(cls, search_text_list, limit=model_conf.MAX_FETCH_RECORD_FULL_TEXT_SEARCH_PER_PAGE):
        
        logging.debug('full_text_count: search_text_list=%s', search_text_list)
        
        lowercase_words_list = [x.lower() for x in search_text_list]
        
        logging.debug('full_text_search: lowercase_words_list=%s', lowercase_words_list)
        
        query = cls.query()
        
        for word in lowercase_words_list:
            query = query.filter(cls.full_text_search_field == word)
        
        return query.count(limit=limit, keys_only=True)
            
           
        
    @classmethod
    def full_text_search(cls, text_search = None, offset=0,  start_cursor=None, return_with_cursor=False, keys_only=False, 
                         limit=model_conf.MAX_FETCH_RECORD_FULL_TEXT_SEARCH_PER_PAGE):
        
        logging.debug('full_text_search: text_search=%s', text_search)
        logging.debug('full_text_search: start_cursor=%s', start_cursor)
        
        
        query = cls.query()
        if text_search:
            lowercase_words_list = [x.lower() for x in text_search]
            
            logging.debug('full_text_search: lowercase_words_list=%s', lowercase_words_list)
            
            for word in lowercase_words_list:
                query = query.filter(cls.full_text_search_field == word)
        
        if start_cursor or return_with_cursor:
            if is_not_empty(start_cursor):
                if isinstance(start_cursor, string_types):
                    start_cursor = Cursor.from_websafe_string(start_cursor)
            else:
                start_cursor = None
            
            (search_results, next_cursor, more)       = query.fetch_page(page_size=limit, start_cursor=start_cursor, keys_only=keys_only)
            logging.debug('##########################################')
            
            logging.debug('full_text_search: search_results=%s', search_results)
            logging.debug('full_text_search: next_cursor=%s', next_cursor)
            logging.debug('full_text_search: more=%s', more) 
            
            logging.debug('##########################################')
            
            if more:
                return search_results, next_cursor.to_websafe_string().decode('utf-8')  
            else:    
                return search_results, 'None'
            
        else:
            search_results = query.fetch(limit=limit, offset=offset)
            
            return search_results        
            

    
