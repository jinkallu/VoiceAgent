from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from resource_mgmt import ResourceManagement
from storage_mgmt import StorageManagement
from blob_ops import BlobOps
from container_mgmt import ContainerManagement
from loganalytics_mgmt import LogAnalyticsMgmt
from container_reg_mgmt import ContainerRegistryMgmt

import random
import string

import os
from dotenv import load_dotenv

class AzureOps:
    def __init__(self):
        if not os.environ.get("AZURE_SUBSCRIPTION_ID"):
            load_dotenv()

        self.AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

        default_credential = DefaultAzureCredential()
        credential = default_credential
        self.resourceManagement = ResourceManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.blobOps = BlobOps()
        self.storageManagement = StorageManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.containerManagement = ContainerManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.logAnalyticsMgmt = LogAnalyticsMgmt(credential, self.AZURE_SUBSCRIPTION_ID)
        self.containerRegistryMgmt = ContainerRegistryMgmt(credential, self.AZURE_SUBSCRIPTION_ID)

    def generate_random_alphanumeric(self, length):
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        return ''.join(random.choices(characters, k=length))

    def provision_resources(self, rg_name, location="westeurope"):
        # Create resource group
        # Create Lognalytics workspace
        workspace_name = "test-loganalytics"
        workspace = self.logAnalyticsMgmt.getWorkSpace(rg_name, workspace_name)
        if workspace is None:
            workspace = self.logAnalyticsMgmt.createWorkSpace(rg_name, workspace_name, location)
            if workspace is None:
                # TODO: Manage workspace creation error
                pass
        else:
            print("Log analytics workspace already exists")
        # Create Container Apps Env
        env_name = "test-env"
        env = self.containerManagement.getContainerAppsEnv(rg_name, env_name)
        if env is None:
            shared_key = self.logAnalyticsMgmt.getSharedKeys(rg_name, workspace_name)
            env = self.containerManagement.createContainerEnv(rg_name, env_name, location, workspace.customer_id, shared_key)
            if env is None:
                # TODO: Manage container apps env creation error
                pass
        else:
            print("container apps env already exists")
        # Create blob storage
        storage_account_name = "ppooeejdhgsfsd" # TODO: create random name, as it is global
        storage_account = self.storageManagement.getStorageAccount(rg_name, storage_account_name)
        if storage_account is None:
            storage_account = self.storageManagement.createStorageAccount(rg_name, storage_account_name, location)
            if storage_account is None:
                # TODO: Manage storage account creation error
                pass
        else:
            print("storage account already exists")

        # container registry
        registry_name = None
        for i in range(5):
            registry_name = "test" + self.generate_random_alphanumeric(5)
            if self.containerRegistryMgmt.nameAvailable(registry_name):
                break

        registry = None
        if registry is None:
            #registry = self.containerRegistryMgmt.createContainerRegistry(rg_name, registry_name, location)
            if registry is None:
                # TODO: Manage container registry creation error
                pass
            else:
                print("Created container Registry")
        else:
            print("container registry already exists")


        #Container App
        app_name = "test-app"
        app = self.containerManagement.getContainerApp(rg_name, app_name)
        if app is None:
            shared_key = self.logAnalyticsMgmt.getSharedKeys(rg_name, workspace_name)
            env = self.containerManagement.createContainerApp(self.AZURE_SUBSCRIPTION_ID, rg_name, env_name, app_name, location)
            if env is None:
                # TODO: Manage container apps env creation error
                pass
        else:
            print("container apps env already exists")

        # Create managed identity
        # AI services
        

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
