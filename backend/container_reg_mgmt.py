from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerregistry.models import Registry, Sku
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.containerregistry.models import RegistryNameCheckRequest

class ContainerRegistryMgmt:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.containerRegistry_client = ContainerRegistryManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    def nameAvailable(self, registry_name):
        # Create the check request
        check_request = RegistryNameCheckRequest(name=registry_name, type="Microsoft.ContainerRegistry/registries")
        try:
            # Check availability
            result = self.containerRegistry_client.registries.check_name_availability(check_request)
            return  result.name_available
        except:
            print("Unknown error in checking registry name availability")
            return None

    def getContainerRegistry(self, rg_name, registry_name):
        try:
            registry = self.containerRegistry_client.registries.get(rg_name, registry_name)
            print(f"✅ Container Registry '{registry_name}' exists.")
            return registry
        except ResourceNotFoundError:
            print(f"❌ Container Registry '{registry_name}' does NOT exist.")
            return False


    def createContainerRegistry(self, rg_name, registry_name, location):
        # Create the container registry
        try:
            poller = self.containerRegistry_client.registries.begin_create(
                resource_group_name=rg_name,
                registry_name=registry_name,
                registry=Registry(
                    location=location,
                    sku=Sku(name="Basic"),  # Basic | Standard | Premium
                    admin_user_enabled=True  # Optional: enables admin username/password auth
                )
            )

            registry = poller.result()
            return registry
        except ResourceNotFoundError:
            print(f"Container registry '{registry_name}' creation failed")

