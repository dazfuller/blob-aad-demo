# AAD based Azure blob access

This is a simple python application which connects to an azure storage account using
AAD based authentication and then writes a simple file.

The application requires a configuration file called `appsettings.json` which has the
following structure.

```json
{
    "tenantId": "<tenant id>",
    "clientId": "<azure ad application id>",
    "clientSecret": "<azure ad application secret>"
}
```

Permissions are described in the [Authenticate access to Azure blobs and queues using Azure Active Directory](https://docs.microsoft.com/azure/storage/common/storage-auth-aad) documentation.

In order for the solution to work an application needs to be created and then given
`Storage Blob Data Contributor` permissions to a container. These permissions could be
applied at the storage account level as well. When applied at the container level any
call above container level (such as listing containers) will fail.