from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from resource_mgmt import ResourceManagement
from storage_mgmt import StorageManagement
from blob_ops import BlobOps
from container_mgmt import ContainerManagement
from loganalytics_mgmt import LogAnalyticsMgmt

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
        self.containerManagement = ContainerManagement(credential, AZURE_SUBSCRIPTION_ID)
        self.logAnalyticsMgmt = LogAnalyticsMgmt(credential, AZURE_SUBSCRIPTION_ID)

    def provision_resources(self, rg_name, location="westeurope"):
        # Create resource group
        # Create Lognalytics workspace
        workspace_name = "test-loganalytics"
        workspace = self.logAnalyticsMgmt.createWorkSpace(rg_name, workspace_name, location)
        if workspace is None:
            # TODO: Manage error
            pass
        # Create Container Apps Env
        env_name = "test-env"
        shared_key = self.logAnalyticsMgmt.getSharedKeys(rg_name, workspace_name)
        env = self.containerManagement.createContainerEnv(rg_name, env_name, location, workspace.customer_id, shared_key)
        if env is None:
            # TODO: Manage error
            pass
        # Create blob storage
        # Create managed identity
        # container registry
        # AI services
        # Container App

def test_create_container_env(azure_ops):
    azure_ops.containerManagement.createContainerEnv("test", "test-env", "westeurope")




if __name__ == "__main__":
    azure_ops = AzureOps()
    azure_ops.provision_resources("test")
    #azure_ops.resourceManagement.list_resource_groups()
    #azure_ops.resourceManagement.createResourceGroup("test", "westeurope")
    #azure_ops.resourceManagement.list_resource_groups()
    #azure_ops.storageManagement.createStorageAccount("test", "ppooeejdhgsfsd", "westeurope")
    #print(azure_ops.containerManagement.getContainerAppURL("rg-testagent5", "capps-backend-s2kzrdow3y3rq"))
    #test_create_container_env(azure_ops)
    #azure_ops.logAnalyticsMgmt.test_getSharedKeys("test", "test-log-analytics")
