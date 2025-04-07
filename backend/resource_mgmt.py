from azure.mgmt.resource import ResourceManagementClient


class ResourceManagement:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):

        # Initialize the ResourceManagementClient with your Azure subscription ID
        #subscription_id = "<your-subscription-id>"  # Replace with your Azure subscription ID
        self.client = ResourceManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    # List resource groups
    def list_resource_groups(self):
        print("List Resources")
        groups = self.client.resource_groups.list()
        resource_groups = []
        for rg in groups:
            print(f"Resource Group Name: {rg.name}, Location: {rg.location}")
            #resources_in_group = self.list_resources_in_group(rg.name)
            resource_groups.append({"name": rg.name, "location": rg.location})

        return resource_groups
    
    def list_resources_in_group(self, resource_group_name):
        resources = self.client.resources.list_by_resource_group(resource_group_name)
        return [
            {
                "name": res.name,
                "type": res.type,
                "location": res.location
            }
            for res in resources
        ]   
    
    def filter_resources_by_type(self, resources, resource_type):
        return [
            {
                "name": res['name'],
                "type": res['type'],
                "location": res['location']
            }
            for res in resources if res['type'] == resource_type
        ]


    def get_blobstorage_from_resource_group(self, resource_group_name):
        resources = self.list_resources_in_group(resource_group_name)
        print("resources", resources)
        resource_type = 'Microsoft.Storage/storageAccounts'
        blob_storage = self.filter_resources_by_type(resources, resource_type)
        return blob_storage
        #return self.client.resources.get(resource_group_name, resource_type)
        #self.client.resources.

    def createResourceGroup(self, rg_name, location):
        try:
            # Create the resource group
            resource_group_params = {"location": location}
            self.client.resource_groups.create_or_update(rg_name, resource_group_params)
            return True
        except:
            print("Error in creating rg")

    def getResourceGroup(self, rg_name):
        try:
            # Get resource group details
            resource_group = self.client.resource_groups.get(rg_name)
            return resource_group
        except:
            return None
        
    def register_eventgrid_provider(self):
        provider_namespace = "Microsoft.EventGrid"
        
        try:
            # Register the Microsoft.EventGrid resource provider
            poller = self.client.providers.register(provider_namespace)
            
            # Wait for the registration to complete
            poller.wait()  # This will block until the registration is complete
            
            print(f"The {provider_namespace} provider is successfully registered.")
            return True
        except Exception as e:
            print(f"Error registering the provider: {e}")
            return False



         


if __name__ == "__main__":
    listResources = ResourceManagement()
    listResources.list_resource_groups()

    pass
    #list_resource_groups()
