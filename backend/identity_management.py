from azure.mgmt.msi import ManagedServiceIdentityClient
from azure.mgmt.msi.models import Identity

class IdentityManagement:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.client = ManagedServiceIdentityClient(credential, AZURE_SUBSCRIPTION_ID)

    def createManagedIdentity(self, rg_name, identity_name, location):
        try:
            identity = self.client.user_assigned_identities.create_or_update(
                    resource_group_name=rg_name,
                    resource_name=identity_name,
                    parameters=Identity(location=location)
                )
            return identity
        except Exception as e:
            print(f"Error in creation of identity{e}")

    def getManagedIdentity(self, rg_name, identity_name):
        try:
            # Get the User Assigned Managed Identity
            identity = self.client.user_assigned_identities.get(
                resource_group_name=rg_name,
                resource_name=identity_name
            )
            return identity
        except:
            print("Could not access managed identity")
