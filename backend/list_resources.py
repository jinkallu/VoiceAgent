from azure.mgmt.resource import ResourceManagementClient

import os
from dotenv import load_dotenv

class ListResources:
    def __init__(self, credential):
        if not os.environ.get("AZURE_SUBSCRIPTION_ID"):
            load_dotenv()

        AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

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
        resource_type = 'Microsoft.Storage/storageAccounts'
        blob_storage = self.filter_resources_by_type(resources, resource_type)
        return blob_storage
        #return self.client.resources.get(resource_group_name, resource_type)
        #self.client.resources.
         


if __name__ == "__main__":
    listResources = ListResources()
    listResources.list_resource_groups()
    pass
    #list_resource_groups()
