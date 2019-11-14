import json

from typing import Dict

from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from azure.identity import ClientSecretCredential


# Load the client credentials from the configuration file
with open('appsettings.json', 'r') as f:
    config: Dict = json.load(f)

# CHANGE these for your our storage account details
SA_NAME: str = 'polydataswtusysohtfec'
CONTAINER: str = 'demo'


def run():
    tenant_id: str = config["tenantId"]
    client_id: str = config['clientId']
    client_secret: str = config['clientSecret']

    # Authenticate with the AAD service principal
    credential: ClientSecretCredential = ClientSecretCredential(
        tenant_id,
        client_id,
        client_secret)

    # Create a new block blob service instance
    blob_service: BlobServiceClient = BlobServiceClient(
        account_url=f'https://{SA_NAME}.blob.core.windows.net',
        credential=credential
    )

    # Check to see if the test file exists, if so the delete it
    container_client: ContainerClient

    if CONTAINER in [c.name for c in blob_service.list_containers()]:
        print('Container already exists')
        container_client = blob_service.get_container_client(CONTAINER)
    else:
        print('Creating container')
        container_client = blob_service.create_container(CONTAINER)

    # Create a new blob from text
    print('Uploading blob data')
    blob_client: BlobClient = container_client.get_blob_client('test.txt')
    data: bytes = 'Hello world from your friendly service principal'\
        .encode('utf-8')
    blob_client.upload_blob(data, blob_type='BlockBlob', length=len(data),
                            overwrite=True)


if __name__ == "__main__":
    run()
