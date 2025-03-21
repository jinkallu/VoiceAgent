from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from list_resources import ListResources
from blob_ops import BlobOps

class AzureOps:
    def __init__(self):
        default_credential = DefaultAzureCredential()
        credential = default_credential
        self.listResources = ListResources(credential)
        self.blobOps = BlobOps()