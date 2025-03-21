from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from resource_mgmt import ResourceManagement
from storage_mgmt import StorageManagement
from blob_ops import BlobOps

import os
from dotenv import load_dotenv

class AzureOps:
    def __init__(self):
        if not os.environ.get("AZURE_SUBSCRIPTION_ID"):
            load_dotenv()

        AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

        default_credential = DefaultAzureCredential()
        credential = default_credential
        self.resourceManagement = ResourceManagement(credential, AZURE_SUBSCRIPTION_ID)
        self.blobOps = BlobOps()
        self.storageManagement = StorageManagement(credential, AZURE_SUBSCRIPTION_ID)

if __name__ == "__main__":
    azure_ops = AzureOps()
    azure_ops.resourceManagement.list_resource_groups()
    #azure_ops.resourceManagement.createResourceGroup("test", "westeurope")
    #azure_ops.resourceManagement.list_resource_groups()
    azure_ops.storageManagement.createStorageAccount("test", "ppooeejdhgsfsd", "westeurope")

