import json

from typing import Dict

import adal
from azure.storage.blob import BlockBlobService
from azure.storage.common import TokenCredential


# Load the client credentials from the configuration file
with open('appsettings.json', 'r') as f:
    config: Dict = json.load(f)

RESOURCE: str = 'https://storage.azure.com/'

# 
# Change these for your storage account details
# 
SA_NAME: str = 'blobaaddemo'
CONTAINER: str = 'demo'

authority_url: str = f'https://login.microsoftonline.com/{config["tenantId"]}'
client_id: str = config['clientId']
client_secret: str = config['clientSecret']

# Authenticate with the AAD service principal and retrieve the access token
context: adal.AuthenticationContext = adal.AuthenticationContext(authority_url)
token: Dict = context.acquire_token_with_client_credentials(
    RESOURCE,
    client_id,
    client_secret
)
access_token: TokenCredential = TokenCredential(token['accessToken'])

# Create a new block blob service instance
blob_service: BlockBlobService = BlockBlobService(SA_NAME, token_credential=access_token)

# Check to see if the test file exists, if so the delete it
if blob_service.exists(CONTAINER, 'test.txt'):
    blob_service.delete_blob(CONTAINER, 'test.txt')

# Create a new blob from text
blob_service.create_blob_from_text(CONTAINER, 'test.txt', text='Hello world from your friendly service principal')
print('Blob created')
