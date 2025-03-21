from azure.mgmt.storage import StorageManagementClient

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
            return True
        except:
            print("Error in creating storage account")
