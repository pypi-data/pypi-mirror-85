import os


INTERNAL_MAX_FETCH_RECORD                       = 9999
MAX_FETCH_RECORD_FULL_TEXT_SEARCH               = 1000
MAX_FETCH_RECORD_FULL_TEXT_SEARCH_PER_PAGE      = 10
MAX_FETCH_RECORD                                = 99999999
MAX_FETCH_IMAGE_RECORD                          = 100
MAX_CHAR_RANDOM_UUID4                           = 20
PAGINATION_SIZE                                 = 2
VISIBLE_PAGE_COUNT                              = 10

GENDER_MALE_CODE                                = 'm'
GENDER_FEMALE_CODE                              = 'f'

APPLICATION_ACCOUNT_PROVIDER                    = 'app'

MODEL_PROJECT_ID                                = os.environ['GCLOUD_PROJECT_ID']

DATASTORE_SERVICE_ACCOUNT_KEY_FILEPATH          = 'gae-service-account-key.json'

DATASTORE_CREDENTIAL_PATH                       = os.path.abspath(os.path.dirname(__file__)) + '/../' + DATASTORE_SERVICE_ACCOUNT_KEY_FILEPATH