from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
from resource_mgmt import ResourceManagement
from storage_mgmt import StorageManagement
from blob_ops import BlobOps
from container_mgmt import ContainerManagement
from loganalytics_mgmt import LogAnalyticsMgmt
from container_reg_mgmt import ContainerRegistryMgmt
from identity_management import IdentityManagement
from cogni_services_mgmt import CognitiveServicesMgmt

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
        self.identityManagement = IdentityManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.cognitiveServicesMgmt = CognitiveServicesMgmt(credential, self.AZURE_SUBSCRIPTION_ID)

    def generate_random_alphanumeric(self, length):
        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        return ''.join(random.choices(characters, k=length))
    
    def get_resource_names_by_type(self, newresources, target_type):
        return [res["name"] for res in newresources if res["type"].lower() == target_type.lower()]


    def provision_resources(self, rg_name, location="eastus 2"):
        # Create resource group
        resource_group = self.resourceManagement.getResourceGroup(rg_name)
        if resource_group is None:
            resource_group = self.resourceManagement.createResourceGroup(rg_name, location)
            if resource_group is None:
                # TODO: Manage resource_group creation error
                pass
        else:
            print("resource_group already exists")

        # Get already existing resources in teh resource group
        resources = self.resourceManagement.list_resources_in_group(rg_name)
        
        workspace_names = self.get_resource_names_by_type(resources, 'Microsoft.OperationalInsights/workspaces')
        workspace_name = "test-loganalytics"
        workspace = None
        if len(workspace_names) > 0:
            workspace_name = workspace_names[0]
            print("Log analytics workspace already exists")
            workspace = self.logAnalyticsMgmt.getWorkSpace(rg_name, workspace_name)
            if workspace is None:
                print("Error in Accessing Log analytics workspace")
            else:
                print("Accessed Log analytics workspace")
        else: # No workspace exist
            # Create Lognalytics workspace
            workspace = self.logAnalyticsMgmt.createWorkSpace(rg_name, workspace_name, location)
            if workspace is None:
                # TODO: Manage workspace creation error
                pass

        
        container_app_env_names = self.get_resource_names_by_type(resources, "Microsoft.App/managedEnvironments")    
        # Create Container Apps Env
        env_name = "test-env"
        env = None
        if len(container_app_env_names) > 0:
            env_name = container_app_env_names[0]
            print("container apps env already exists")
            env = self.containerManagement.getContainerAppsEnv(rg_name, env_name)
            if env is None:
                print("Error in Accessing container apps env")
            else:
                print("Accessed container apps env")
        else:
            shared_key = self.logAnalyticsMgmt.getSharedKeys(rg_name, workspace_name)
            env = self.containerManagement.createContainerEnv(rg_name, env_name, location, workspace.customer_id, shared_key)
            if env is None:
                # TODO: Manage container apps env creation error
                pass
     
        # Create blob storage
        storage_account_names = self.get_resource_names_by_type(resources, "Microsoft.Storage/storageAccounts")
        storage_account_name = "test" + self.generate_random_alphanumeric(5)
        storage_account = None
        if len(storage_account_names) > 0:
            storage_account_name = storage_account_names[0]
            print("storage account already exists")
            storage_account = self.storageManagement.getStorageAccount(rg_name, storage_account_name)
            if storage_account is None:
                print("Error in Accessing storage account")
            else:
                print("Accessed storage account")
        else:
            storage_account = self.storageManagement.createStorageAccount(rg_name, storage_account_name, location)
            if storage_account is None:
                # TODO: Manage storage account creation error
                pass

        # container registry
        registry_names = self.get_resource_names_by_type(resources, "Microsoft.ContainerRegistry/registries")
        registry_name = None
        registry = None
        if len(registry_names) > 0:
            registry_name = registry_names[0]
            print("container registry already exists")
            registry = self.containerRegistryMgmt.getContainerRegistry(rg_name, registry_name)
            if registry is None:
                print("Error in Accessing container registry")
            else:
                print("Accessed container registry")
        else:
            for i in range(10):
                registry_name = "test" + self.generate_random_alphanumeric(5)
                if self.containerRegistryMgmt.nameAvailable(registry_name):
                    break
            registry = self.containerRegistryMgmt.createContainerRegistry(rg_name, registry_name, location)
            if registry is None:
                # TODO: Manage container registry creation error
                pass

        #Container App
        app_names = self.get_resource_names_by_type(resources, "Microsoft.App/containerApps")
        app_name = "test-app"
        app = None
        if len(app_names) > 0:
            app_name = app_names[0]
            print("container app already exists")
            app = self.containerManagement.getContainerApp(rg_name, app_name)
            if app is None:
                print("Error in Accessing app")
            else:
                print("Accessed app")
        else:
            app = self.containerManagement.createContainerApp(self.AZURE_SUBSCRIPTION_ID, rg_name, env_name, app_name, location)
            if app is None:
                # TODO: Manage container apps env creation error
                pass

        # Create managed identity
        identity_names = self.get_resource_names_by_type(resources, "Microsoft.ManagedIdentity/userAssignedIdentities")
        identity_name = "test-identity"
        identity = None
        if len(identity_names) > 0:
            identity_name = identity_names[0]
            print("Identity already exists")
            identity = self.identityManagement.getManagedIdentity(rg_name, identity_name)
            if identity is None:
                print("Error in Accessing identity")
            else:
                print("Accessed identity")
        else:
            identity = self.identityManagement.createManagedIdentity(rg_name, identity_name, location)
            if identity is None:
                # TODO: Manage identity creation error
                pass
        # AI services
        aiservice_names =  self.get_resource_names_by_type(resources, "Microsoft.CognitiveServices/accounts")
        aiservice_name = "testOAI1"
        aiservice = None
        if len(aiservice_names) > 0:
            aiservice_name = aiservice_names[0]
            print(f"aiservice {aiservice_name} already exists")
            aiservice = self.cognitiveServicesMgmt.getAIService(rg_name, aiservice_name)
            if aiservice is None:
                print("Error in Accessing aiservice")
            else:
                print("Accessed aiservice")
        else:
            aiservice = self.cognitiveServicesMgmt.createServiceResource(rg_name, aiservice_name, location)
            if aiservice is None:
                # TODO: Manage identity creation error
                pass

        # AI Deployments
        deployment_name = "gpt-4o"
        deployment = self.cognitiveServicesMgmt.getDeployment(rg_name, aiservice_name, deployment_name)
        if deployment is None:
            model_name = "gpt-4o"
            version = "2024-11-20"
            capacity = 20
            deployment = self.cognitiveServicesMgmt.createDeployment(rg_name, aiservice_name, location, deployment_name, model_name, version, capacity)
            if deployment is None:
                # TODO: Manage deployment creation error
                pass

        # AI Deployments
        deployment_name = "gpt-4o-mini"
        deployment = self.cognitiveServicesMgmt.getDeployment(rg_name, aiservice_name, deployment_name)
        if deployment is None:
            model_name = "gpt-4o-mini"
            version = "2024-07-18"
            capacity = 20
            deployment = self.cognitiveServicesMgmt.createDeployment(rg_name, aiservice_name, location, deployment_name, model_name, version, capacity)
            if deployment is None:
                # TODO: Manage deployment creation error
                pass

        
        

def test_create_container_env(azure_ops):
    azure_ops.containerManagement.createContainerEnv("test", "test-env", "eastus 2")




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
