from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

import os
from dotenv import load_dotenv

class ListResources:
    def __init__(self):
        # Authenticate using DefaultAzureCredential
        credential = DefaultAzureCredential()

        if not os.environ.get("AZURE_SUBSCRIPTION_ID"):
            load_dotenv()

        AZURE_SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

        # Initialize the ResourceManagementClient with your Azure subscription ID
        #subscription_id = "<your-subscription-id>"  # Replace with your Azure subscription ID
        self.client = ResourceManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    # List resource groups
    def list_resource_groups(self):
        print("List Resources")
        resource_groups = self.client.resource_groups.list()
        resource_groups = []
        for rg in resource_groups:
            print(f"Resource Group Name: {rg.name}, Location: {rg.location}")
            resource_groups.append({"name": rg.name, "location": rg.location})

        self.client.close()  # Close the client properly
        return resource_groups
            

if __name__ == "__main__":
    listResources = ListResources()
    listResources.list_resource_groups()
    pass
    #list_resource_groups()
