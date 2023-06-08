from storages.backends.azure_storage import AzureStorage
from Diploma_website.settings import DEBUG, BASE_DIR
import os
import json

if DEBUG:
    with open(os.path.join(BASE_DIR, 'config.json')) as config_file:
        configs = json.load(config_file)
else:
    with open('/etc/config.json') as config_file:
        configs = json.load(config_file)

class AzureMediaStorage(AzureStorage):
    account_name = configs['AZ_STORAGE_NAME']
    account_key = configs['AZ_STORAGE_KEY']
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = configs['AZ_STORAGE_NAME']
    account_key = configs['AZ_STORAGE_KEY']
    azure_container = 'static'
    expiration_secs = None