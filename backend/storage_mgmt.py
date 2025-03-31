from azure.mgmt.storage import StorageManagementClient
from azure.core.exceptions import ResourceNotFoundError

class StorageManagement:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.storage_client = StorageManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    def createStorageAccount(self, rg_name, storage_account_name, location):
        params = {
            "location": location,
            "sku": {"name": "Standard_LRS"},
            "kind": "StorageV2",
            "enable_https_traffic_only": True,
        }

        try:
            poller = self.storage_client.storage_accounts.begin_create(
                rg_name, storage_account_name, params
            )
            account_result = poller.result()
            return account_result
        except Exception as e:
            print(f"Error in creating storage account{e}")

    def getStorageAccount(self, rg_name, storage_account_name):
        try:
            account = self.storage_client.storage_accounts.get_properties(rg_name, storage_account_name)
            return account
        except ResourceNotFoundError:
            print("Storage account does not exist.")

