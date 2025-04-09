from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from resource_mgmt import ResourceManagement
from storage_mgmt import StorageManagement
from blob_ops import BlobOps
from containerapp_mgmt import ContainerAppManagement
from loganalytics_mgmt import LogAnalyticsMgmt
from container_reg_mgmt import ContainerRegistryMgmt
from identity_management import IdentityManagement
from cogni_services_mgmt import CognitiveServicesMgmt
from auth_mgmt import AuthManagement
from container_mgmt import ContainerMgmt
from evtgrid_mgmt import EventGridMgmt
import logging
#logging.basicConfig(level=logging.DEBUG)

import random
import string

import os
from dotenv import load_dotenv

load_dotenv()
class AzureOps:
    def __init__(self):

        self.permanent_rg_name = os.environ.get("AZURE_ADMIN_RESOURCE_GROUP")
        self.permanent_rg_acr_name = os.environ.get("ADMIN_ACR_NAME")

        self.AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

        default_credential = DefaultAzureCredential()
        credential = default_credential
        self.resourceManagement = ResourceManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.blobOps = BlobOps()
        self.storageManagement = StorageManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.containerAppManagement = ContainerAppManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.logAnalyticsMgmt = LogAnalyticsMgmt(credential, self.AZURE_SUBSCRIPTION_ID)
        self.containerRegistryMgmt = ContainerRegistryMgmt(credential, self.AZURE_SUBSCRIPTION_ID)
        self.identityManagement = IdentityManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.cognitiveServicesMgmt = CognitiveServicesMgmt(credential, self.AZURE_SUBSCRIPTION_ID)
        self.authManagement = AuthManagement(credential, self.AZURE_SUBSCRIPTION_ID)
        self.containerMgmt = ContainerMgmt(credential, self.AZURE_SUBSCRIPTION_ID)
        self.eventGridMgmt = EventGridMgmt(credential, self.AZURE_SUBSCRIPTION_ID)

    def generate_random_lower_alpha(self, length):
        characters = string.ascii_lowercase # a-z
        return ''.join(random.choices(characters, k=length))

    def generate_random_alphanumeric(self, length):
        characters = string.ascii_lowercase + string.digits  # a-z, 0-9
        return ''.join(random.choices(characters, k=length))
    
    def get_resource_names_by_type(self, newresources, target_type):
        return [res["name"] for res in newresources if res["type"].lower() == target_type.lower()]

    def provision_admin_resources(self, rg_name, location="eastus 2"):
        rg_name = rg_name.lower()
        
        resource_group = self.resourceManagement.getResourceGroup(rg_name)
            
        
        if resource_group is None:
            resource_group = self.resourceManagement.createResourceGroup(rg_name, location)
            if resource_group is None:
                # TODO: Manage resource_group creation error
                pass
        # Get already existing resources in teh resource group
        resources = self.resourceManagement.list_resources_in_group(rg_name)
        
        workspace_names = self.get_resource_names_by_type(resources, 'Microsoft.OperationalInsights/workspaces')
        workspace_name = f"{rg_name}-loganalytics"
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

        # Create managed identity
        identity_names = self.get_resource_names_by_type(resources, "Microsoft.ManagedIdentity/userAssignedIdentities")
        identity_name = f"{rg_name}-identity"
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
            else:
                principal_id = identity.principal_id
                self.authManagement.authAccessToRG(principal_id, rg_name)

        container_app_env_names = self.get_resource_names_by_type(resources, "Microsoft.App/managedEnvironments")    
        # Create Container Apps Env
        env_name = f"{rg_name}-env"
        env = None
        if len(container_app_env_names) > 0:
            env_name = container_app_env_names[0]
            print("container apps env already exists")
            env = self.containerAppManagement.getContainerAppsEnv(rg_name, env_name)
            if env is None:
                print("Error in Accessing container apps env")
            else:
                print("Accessed container apps env")
        else:
            shared_key = self.logAnalyticsMgmt.getSharedKeys(rg_name, workspace_name)
            env = self.containerAppManagement.createContainerEnv(rg_name, env_name, location, workspace.customer_id, shared_key)
            if env is None:
                # TODO: Manage container apps env creation error
                pass

        # Create blob storage
        storage_account_names = self.get_resource_names_by_type(resources, "Microsoft.Storage/storageAccounts")
        storage_account_name = rg_name + self.generate_random_alphanumeric(5)
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
            else:
                self.authManagement.authAccessToStorage(identity.principal_id, rg_name, storage_account_name)
                blobOps = BlobOps()
                blobOps.setBlobServiceClient(storage_account_name)
                blobOps.createContainerIfNotExists(os.getenv("AZURE_ADMIN_CONTAINER_NAME"))

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
                principal_id = identity.principal_id
                try:
                    self.authManagement.authAccessToACR(principal_id, registry_name, rg_name)
                    print("Accessed container registry")
                except Exception as e:
                    print(e)
                
        else:
            for i in range(10):
                registry_name = rg_name + self.generate_random_alphanumeric(5)
                if self.containerRegistryMgmt.nameAvailable(registry_name):
                    break
            registry = self.containerRegistryMgmt.createContainerRegistry(rg_name, registry_name, location)
            if registry is None:
                # TODO: Manage container registry creation error
                pass
            else:
                principal_id = identity.principal_id
                self.authManagement.authAccessToACR(principal_id, registry_name, rg_name)

        #Container App front end
        # app_names = self.get_resource_names_by_type(resources, "Microsoft.App/containerApps")
        # app_frontend_name = f"{rg_name}-app-frontend"
        # app_frontend = None
        # #if len(app_names) > 0: # TODO:
        # if app_frontend:
        #     app_frontend_name = app_names[0]
        #     print("container app already exists")
        #     app_frontend = self.containerAppManagement.getContainerApp(rg_name, app_frontend_name)
        #     if app_frontend is None:
        #         print("Error in Accessing app")
        #     else:
        #         print("Accessed app")
        # else:
        #     env_vars = []
        #     app_frontend = self.containerAppManagement.createContainerApp(self.AZURE_SUBSCRIPTION_ID, rg_name, env_name, app_frontend_name, location, identity_name, os.getenv("ADMIN_ACR_NAME"), os.getenv("ADMIN_IMG_NAME"), os.getenv("ADMIN_IMG_TAG"), env_vars, 3000, True)
        #     if app_frontend is None:
        #         # TODO: Manage container apps env creation error
        #         pass
            
        #Container App
        app_names = self.get_resource_names_by_type(resources, "Microsoft.App/containerApps")
        app_name = f"{rg_name}-app"
        app = None
        #if len(app_names) > 0: # TODO:
        if app:
            app_name = app_names[0]
            print("container app already exists")
            app = self.containerAppManagement.getContainerApp(rg_name, app_name)
            if app is None:
                print("Error in Accessing app")
            else:
                print("Accessed app")
        else:
            env_vars = [
                            {
                                "name": "OPENAI_4O_MINI_ENDPOINT", 
                                "value": os.getenv("OPENAI_4O_MINI_ENDPOINT")
                            },
                            {
                                "name": "OPENAI_4O_MINI_KEY", 
                                "value": os.getenv("OPENAI_4O_MINI_KEY")
                            },
                            {
                                "name": "OPENAI_4O_ENDPOINT", 
                                "value": os.getenv("OPENAI_4O_ENDPOINT")
                            },
                            {
                                "name": "OPENAI_4O_KEY", 
                                "value": os.getenv("OPENAI_4O_KEY")
                            },
                            {
                                "name": "AZURE_CLIENT_ID", 
                                "value": identity.client_id
                            },
                            {
                                "name": "AZURE_STORAGE_ENDPOINT",
                                "value": f"https://{storage_account_name}.blob.core.windows.net"
                            },
                            {
                                "name": "ADMIN_RG_NAME", 
                                "value": os.getenv("ADMIN_RG_NAME")
                            },
                            {
                                "name": "ADMIN_ACR_NAME", 
                                "value": os.getenv("ADMIN_ACR_NAME")
                            },
                            {
                                "name": "ADMIN_IMG_NAME", 
                                "value": os.getenv("ADMIN_IMG_NAME")
                            },
                            {
                                "name": "ADMIN_IMG_TAG", 
                                "value": os.getenv("ADMIN_IMG_TAG")
                            },
                            {
                                "name": "ADMIN_IMG_LOCATION", 
                                "value": os.getenv("ADMIN_IMG_LOCATION")
                            },
                            {
                                "name": "ASSISTANT_IMG_NAME", 
                                "value": os.getenv("ASSISTANT_IMG_NAME")
                            },
                            {
                                "name": "ASSISTANT_IMG_TAG", 
                                "value": os.getenv("ASSISTANT_IMG_TAG")
                            },
                            {
                                "name": "TTS_IMG_NAME", 
                                "value": os.getenv("TTS_IMG_NAME")
                            },
                            {
                                "name": "TTS_IMG_TAG", 
                                "value": os.getenv("TTS_IMG_TAG")
                            },
                            {
                                "name": "STT_IMG_NAME", 
                                "value": os.getenv("STT_IMG_NAME")
                            },
                            {
                                "name": "STT_IMG_TAG", 
                                "value": os.getenv("STT_IMG_TAG")
                            },
                            {
                                "name": "DEFAULT_PRODUCT_CONTAINER", 
                                "value": os.getenv("DEFAULT_PRODUCT_CONTAINER")
                            },
                            {
                                "name": "LOG_CONTAINER", 
                                "value": os.getenv("LOG_CONTAINER")
                            },
                            {
                                "name": "AZURE_ADMIN_RESOURCE_GROUP", 
                                "value": os.getenv("AZURE_ADMIN_RESOURCE_GROUP")
                            },
                            {
                                "name": "AZURE_ADMIN_CONTAINER_NAME", 
                                "value": os.getenv("AZURE_ADMIN_CONTAINER_NAME")
                            },
                            {
                                "name": "AZURE_ADMIN_BLOB_NAME", 
                                "value": os.getenv("AZURE_ADMIN_BLOB_NAME")
                            },
                            {
                                "name": "ALLOWED_CLOUD_ORIGIN", 
                                "value": os.getenv("ALLOWED_CLOUD_ORIGIN")
                            },
                     
                        ]
            app = self.containerAppManagement.createContainerApp(self.AZURE_SUBSCRIPTION_ID, rg_name, env_name, app_name, location, identity_name, os.getenv("ADMIN_ACR_NAME"), os.getenv("ADMIN_IMG_NAME"), os.getenv("ADMIN_IMG_TAG"), env_vars, 8000, False)
            if app is None:
                # TODO: Manage container apps env creation error
                pass


    def provision_resources(self, assistant_name, user_name, location="eastus 2"):
        resource_group = None
        rg_name = ""
        for i in range(100):
            rg_name = self.generate_random_lower_alpha(6)
            resource_group = self.resourceManagement.getResourceGroup(rg_name)
            if resource_group:
                continue
            else:
                break

        if resource_group:
            print("Could not generate resource group name, it already exists")
            return
        # Create resource group
        if resource_group is None:
            resource_group = self.resourceManagement.createResourceGroup(rg_name, location)
            if resource_group is None:
                # TODO: Manage resource_group creation error
                pass
            else: # update users.json with this resource
                blob_storage = self.resourceManagement.get_blobstorage_from_resource_group(os.getenv("AZURE_ADMIN_RESOURCE_GROUP"))
                print(blob_storage)
                if(len(blob_storage)>0):
                    storageName=blob_storage[0]["name"]
                    self.blobOps.setBlobServiceClient(storage_name=storageName)
                    self.blobOps.setContainerClient(os.getenv("AZURE_ADMIN_CONTAINER_NAME"))

                    userData=self.blobOps.getStorageMappingAsJson(os.getenv("AZURE_ADMIN_BLOB_NAME"))

                    user = next((u for u in userData if u["username"] == user_name), None)
                    if user:
                        user["resourceGroups"].append({"assistant-name": assistant_name, "rg-name": rg_name, "app-url":None})
                        try:
                            res=self.blobOps.createOrReplaceBlobFromPyDict(os.getenv("AZURE_ADMIN_BLOB_NAME"), userData)
                            print(res)
                        except Exception as e:
                            print(e)

                    

        else:
            print("resource_group already exists")

        # Get already existing resources in teh resource group
        resources = self.resourceManagement.list_resources_in_group(rg_name)
        
        workspace_names = self.get_resource_names_by_type(resources, 'Microsoft.OperationalInsights/workspaces')
        workspace_name = f"{rg_name}-loganalytics"
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

        # Create managed identity
        identity_names = self.get_resource_names_by_type(resources, "Microsoft.ManagedIdentity/userAssignedIdentities")
        identity_name = f"{rg_name}-identity"
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
            else:
                principal_id = identity.principal_id
                self.authManagement.authAccessToACR(principal_id, self.permanent_rg_acr_name, self.permanent_rg_name)
                #self.authManagement.authAccessToRG(principal_id, rg_name)
                #self.authManagement.authAccessToStorage(principal_id, rg_name, storage_account_name)
                # self.containerAppManagement.assign_identity_to_containerapp(rg_name, app_name, identity_name)
                # env_vars = [
                #     {
                #         "name": "AZURE_OPENAI_ENDPOINT",
                #         "value": os.getenv("AZURE_OPENAI_ENDPOINT")
                #     },
                #     {
                #         "name": "AZURE_OPENAI_REALTIME_DEPLOYMENT",
                #         "value": os.getenv("AZURE_OPENAI_REALTIME_DEPLOYMENT")
                #     },
                #     {
                #         "name": "AZURE_OPENAI_REALTIME_VOICE_CHOICE",
                #         "value": os.getenv("AZURE_OPENAI_REALTIME_VOICE_CHOICE")
                #     },
                #     {
                #         "name": "AZURE_TENANT_ID",
                #         "value": os.getenv("AZURE_TENANT_ID")
                #     },
                #     {
                #         "name": "AZURE_STORAGE_ENDPOINT",
                #         "value": f"https://{storage_account_name}.blob.core.windows.net"
                #     },
                    
                # ]
                # self.containerAppManagement.updateContainerApp(rg_name, app_name, os.getenv("PERMANENT_ACR_NAME"), os.getenv("PERMANENT_IMG_NAME"), os.getenv("PERMANENT_IMG_TAG"), os.getenv("PERMANENT_IMG_LOCATION"), env_name, identity_name, env_vars)

        
        container_app_env_names = self.get_resource_names_by_type(resources, "Microsoft.App/managedEnvironments")    
        # Create Container Apps Env
        env_name = f"{rg_name}-env"
        env = None
        if len(container_app_env_names) > 0:
            env_name = container_app_env_names[0]
            print("container apps env already exists")
            env = self.containerAppManagement.getContainerAppsEnv(rg_name, env_name)
            if env is None:
                print("Error in Accessing container apps env")
            else:
                print("Accessed container apps env")
        else:
            shared_key = self.logAnalyticsMgmt.getSharedKeys(rg_name, workspace_name)
            env = self.containerAppManagement.createContainerEnv(rg_name, env_name, location, workspace.customer_id, shared_key)
            if env is None:
                # TODO: Manage container apps env creation error
                pass
     
        # Create blob storage
        storage_account_names = self.get_resource_names_by_type(resources, "Microsoft.Storage/storageAccounts")
        storage_account_name = rg_name + self.generate_random_alphanumeric(5)
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
            else:
                self.authManagement.authAccessToStorage(os.getenv("AZURE_ADMIN_ID_PRINCIPAL_ID"), rg_name, storage_account_name)
                self.authManagement.authAccessToStorage(identity.principal_id, rg_name, storage_account_name)
                blobOps = BlobOps()
                blobOps.setBlobServiceClient(storage_account_name)
                blobOps.createContainerIfNotExists(os.getenv("LOG_CONTAINER"))
                default_prd_container = os.getenv("DEFAULT_PRODUCT_CONTAINER") # TODO: manage it in env
                if blobOps.createContainerIfNotExists(default_prd_container):
                    blobOps.setContainerClient(default_prd_container)
                    blob_name = os.getenv("PRODUCT_DATA_FILE_NAME")  # Name of the blob you're uploading
                    file_path = os.getenv("DEFAULT_PRODUCT_DATA_PATH")  # Local path to your JSON file
                    print(file_path)
                    with open(file_path, "rb") as data:
                        print('File opened')
                        blobOps.createOrUpdateBlob(blob_name, data)

        # # container registry
        # registry_names = self.get_resource_names_by_type(resources, "Microsoft.ContainerRegistry/registries")
        # registry_name = None
        # registry = None
        # if len(registry_names) > 0:
        #     registry_name = registry_names[0]
        #     print("container registry already exists")
        #     registry = self.containerRegistryMgmt.getContainerRegistry(rg_name, registry_name)
        #     if registry is None:
        #         print("Error in Accessing container registry")
        #     else:
        #         print("Accessed container registry")
        # else:
        #     for i in range(10):
        #         registry_name = rg_name + self.generate_random_alphanumeric(5)
        #         if self.containerRegistryMgmt.nameAvailable(registry_name):
        #             break
        #     registry = self.containerRegistryMgmt.createContainerRegistry(rg_name, registry_name, location)
        #     if registry is None:
        #         # TODO: Manage container registry creation error
        #         pass

        # Speach to text whisperCPP
        # copy container image from public registry to azure registry first
        # az acr import -n testagent5acrs2kzrdow3y3rq --source ghcr.io/ggerganov/whisper.cpp:main -t stt:main                   
        # Then create a container app
        stt_app_name = f"{rg_name}-stt-app"
        stt_app = None
        stt_app_url = None
        env_vars = []
        command = ["build/bin/whisper-server", "--host", "0.0.0.0", "-lpt", "-0.5"]
        stt_app = self.containerAppManagement.createContainerApp(self.AZURE_SUBSCRIPTION_ID, rg_name, env_name, stt_app_name, location, identity_name, os.getenv("ADMIN_ACR_NAME"), os.getenv("STT_IMG_NAME"),  os.getenv("STT_IMG_TAG"), [], 8080, False, command)
        if stt_app is None:
                # TODO: Manage container app creation error
                pass
        else:
            stt_app_url = f"{self.containerAppManagement.getContainerAppURL(rg_name, stt_app_name)}/inference"

        # Text to speach Kokoro
        # az acr import -n testagent5acrs2kzrdow3y3rq --source testbxrbu.azurecr.io/tts-api:latest -t tts:main
        tts_app_name = f"{rg_name}-tts-app"
        tts_app = None
        tts_app_url = None
        env_vars = []
        tts_app = self.containerAppManagement.createContainerApp(self.AZURE_SUBSCRIPTION_ID, rg_name, env_name, tts_app_name, location, identity_name, os.getenv("ADMIN_ACR_NAME"), os.getenv("TTS_IMG_NAME"),  os.getenv("TTS_IMG_TAG"), [], 80, False)
        if tts_app is None:
                # TODO: Manage container app creation error
                pass
        else:
            tts_app_url = self.containerAppManagement.getContainerAppURL(rg_name, tts_app_name)

        #Container App
        app_names = self.get_resource_names_by_type(resources, "Microsoft.App/containerApps")
        app_name = f"{rg_name}-app"
        app = None
        #if len(app_names) > 0: # TODO:
        if app:
            app_name = app_names[0]
            print("container app already exists")
            app = self.containerAppManagement.getContainerApp(rg_name, app_name)
            if app is None:
                print("Error in Accessing app")
            else:
                print("Accessed app")
        else:
            env_vars = [
                            {
                                "name": "OPENAI_4O_MINI_ENDPOINT", 
                                "value": os.getenv("OPENAI_4O_MINI_ENDPOINT")
                            },
                            {
                                "name": "OPENAI_4O_MINI_KEY", 
                                "value": os.getenv("OPENAI_4O_MINI_KEY")
                            },
                            {
                                "name": "OPENAI_4O_ENDPOINT", 
                                "value": os.getenv("OPENAI_4O_ENDPOINT")
                            },
                            {
                                "name": "OPENAI_4O_KEY", 
                                "value": os.getenv("OPENAI_4O_KEY")
                            },
                            {
                                "name": "AZURE_CLIENT_ID", 
                                "value": identity.client_id
                            },
                            {
                                "name": "AZURE_STORAGE_ENDPOINT",
                                "value": f"https://{storage_account_name}.blob.core.windows.net"
                            },
                            {
                                "name": "KOKORO_TTS_URL",
                                "value": tts_app_url
                            },
                            {
                                "name": "WHISPER_STT_URL",
                                "value": stt_app_url
                            },
                        ]
            app = self.containerAppManagement.createContainerApp(self.AZURE_SUBSCRIPTION_ID, rg_name, env_name, app_name, location, identity_name, os.getenv("ADMIN_ACR_NAME"), os.getenv("ASSISTANT_IMG_NAME"), os.getenv("ASSISTANT_IMG_TAG"), env_vars, 8000, True)
            if app is None:
                # TODO: Manage container apps env creation error
                pass
            else:
                app_url = self.containerAppManagement.getContainerAppURL(rg_name, app_name)
                blob_storage = self.resourceManagement.get_blobstorage_from_resource_group(os.getenv("AZURE_ADMIN_RESOURCE_GROUP"))
                print(blob_storage)
                if(len(blob_storage)>0):
                    storageName=blob_storage[0]["name"]
                    self.blobOps.setBlobServiceClient(storage_name=storageName)
                    self.blobOps.setContainerClient(os.getenv("AZURE_ADMIN_CONTAINER_NAME"))

                    userData=self.blobOps.getStorageMappingAsJson(os.getenv("AZURE_ADMIN_BLOB_NAME"))

                    user = next((u for u in userData if u["username"] == user_name), None)
                    if user:
                        if len(user["resourceGroups"]) > 0:
                            user["resourceGroups"][0]["app-url"] = app_url
                            try:
                                res=self.blobOps.createOrReplaceBlobFromPyDict(os.getenv("AZURE_ADMIN_BLOB_NAME"), userData)
                                print(res)
                            except Exception as e:
                                print(e)
                        else:
                            print("Erorr, resourceGroups length")

        

        # AI services
        # aiservice_names =  self.get_resource_names_by_type(resources, "Microsoft.CognitiveServices/accounts")
        # aiservice_name = f"{rg_name}OAI"
        # aiservice = None
        # if len(aiservice_names) > 0:
        #     aiservice_name = aiservice_names[0]
        #     print(f"aiservice {aiservice_name} already exists")
        #     aiservice = self.cognitiveServicesMgmt.getAIService(rg_name, aiservice_name)
        #     if aiservice is None:
        #         print("Error in Accessing aiservice")
        #     else:
        #         print("Accessed aiservice")
        # else:
        #     aiservice = self.cognitiveServicesMgmt.createServiceResource(rg_name, aiservice_name, location)
        #     if aiservice is None:
        #         # TODO: Manage identity creation error
        #         pass

        # AI Deployments
        # deployment_name = "gpt-4o"
        # deployment = self.cognitiveServicesMgmt.getDeployment(rg_name, aiservice_name, deployment_name)
        # if deployment is None:
        #     model_name = "gpt-4o"
        #     version = "2024-11-20"
        #     capacity = 20
        #     deployment = self.cognitiveServicesMgmt.createDeployment(rg_name, aiservice_name, location, deployment_name, model_name, version, capacity)
        #     if deployment is None:
        #         # TODO: Manage deployment creation error
        #         pass

        # # AI Deployments
        # deployment_name = "gpt-4o-mini"
        # deployment = self.cognitiveServicesMgmt.getDeployment(rg_name, aiservice_name, deployment_name)
        # if deployment is None:
        #     model_name = "gpt-4o-mini"
        #     version = "2024-07-18"
        #     capacity = 20
        #     deployment = self.cognitiveServicesMgmt.createDeployment(rg_name, aiservice_name, location, deployment_name, model_name, version, capacity)
        #     if deployment is None:
        #         # TODO: Manage deployment creation error
        #         pass

        
    def restartApp(self, rg_name):
        app_name = f"{rg_name}-app"
        self.containerAppManagement.restartApp(rg_name, app_name)




def test_create_container_env(azure_ops):
    azure_ops.containerAppManagement.createContainerEnv("test", "test-env", "eastus 2")




if __name__ == "__main__":
    azure_ops = AzureOps()
    azure_ops.resourceManagement.register_eventgrid_provider()
    azure_ops.eventGridMgmt.createBlobStorageEvtSubscription("admin", "adminqcr6l", os.getenv("BASE_API_URL")+"/events/", "testevent")
    #azure_ops.provision_resources("myassistant32", "test")
    #azure_ops.provision_admin_resources("Admin")
    # command = ["build/bin/whisper-server", "--host", "0.0.0.0", "-lpt", "-0.5"]
    # app = azure_ops.containerAppManagement.createContainerApp("c5ad8acd-d3b5-4357-beae-caeff17c2d82", "myassistant27", "myassistant27-env", "myassistant27-stt", "east us 2", "myassistant27-identity", os.getenv("PERMANENT_ACR_NAME"), "stt", "main", [], 8080, False, command)

    #print(azure_ops.containerAppManagement.createContainerApp("c5ad8acd-d3b5-4357-beae-caeff17c2d82", "myassistant17", "myassistant17-env", "testapp1", "east us 2").identity.principal_id)
    # azure_ops.authManagement.authAccessToStorage("f24636bc-e888-4ddc-b222-ba55e8083b73", "myassistant14", "myassistant14d8ccj")
    # env_vars = [
    #                 {
    #                     "name": "AZURE_OPENAI_ENDPOINT",
    #                     "value": os.getenv("AZURE_OPENAI_ENDPOINT")
    #                 },
    #                 {
    #                     "name": "AZURE_OPENAI_REALTIME_DEPLOYMENT",
    #                     "value": os.getenv("AZURE_OPENAI_REALTIME_DEPLOYMENT")
    #                 },
    #                 {
    #                     "name": "AZURE_OPENAI_REALTIME_VOICE_CHOICE",
    #                     "value": os.getenv("AZURE_OPENAI_REALTIME_VOICE_CHOICE")
    #                 },
    #                 {
    #                     "name": "AZURE_TENANT_ID",
    #                     "value": os.getenv("AZURE_TENANT_ID")
    #                 },
    #                 {
    #                     "name": "AZURE_STORAGE_ENDPOINT",
    #                     "value": os.getenv("AZURE_STORAGE_ENDPOINT")
    #                 },
    #             ]
    # print(azure_ops.containerAppManagement.updateContainerApp("myassistant17", "testapp1", os.getenv("PERMANENT_ACR_NAME"), os.getenv("PERMANENT_IMG_NAME"), os.getenv("PERMANENT_IMG_TAG"), os.getenv("PERMANENT_IMG_LOCATION"), "myassistant17-env", "myassistant17-identity", env_vars))

    #azure_ops.authManagement.authAccessToACR(identity_principal_id="1373c93f-a342-419d-b42b-8935860e93df", acr_name="testagent5acrs2kzrdow3y3rq", acr_rg_name="rg-testagent5")
    #azure_ops.provision_resources("test")
    #azure_ops.resourceManagement.list_resource_groups()
    #azure_ops.resourceManagement.createResourceGroup("test", "westeurope")
    #azure_ops.resourceManagement.list_resource_groups()
    #azure_ops.storageManagement.createStorageAccount("test", "ppooeejdhgsfsd", "westeurope")
    #print(azure_ops.containerAppManagement.getContainerAppURL("rg-testagent5", "capps-backend-s2kzrdow3y3rq"))
    #test_create_container_env(azure_ops)
    #azure_ops.logAnalyticsMgmt.test_getSharedKeys("test", "test-log-analytics")
