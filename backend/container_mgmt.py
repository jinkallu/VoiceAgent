from azure.mgmt.containerinstance import ContainerInstanceManagementClient
from azure.mgmt.containerinstance.models import ContainerGroup, Container

class ContainerMgmt:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.AZURE_SUBSCRIPTION_ID = AZURE_SUBSCRIPTION_ID
        self.client = ContainerInstanceManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    def updateContainer(self, rg_name, app_name, new_acr_name, new_image_name, new_image_tag, location):
        # Step 2: Get the existing container group
        existing_app = self.client.container_groups.get(rg_name, app_name)

        if existing_app:
            # Step 3: Update the image URL
            new_image_url = f"{new_acr_name}.azurecr.io/{new_image_name}:{new_image_tag}"

            # Step 4: Create the new container with the updated image
            updated_container = Container(
                name=existing_app.containers[0].name,  # Use the existing container's name
                image=new_image_url,  # Set the new image URL from ACR
                resources=existing_app.containers[0].resources  # Keep the same resources as before
            )

            # Step 5: Create a new container group with the updated image
            updated_container_group = ContainerGroup(
                location=location,
                containers=[updated_container],
                os_type=existing_app.os_type,  # Keep the same OS type
                tags=existing_app.tags  # Keep the same tags
            )

            # Step 6: Redeploy the container app with the updated configuration
            redeployed_app = self.client.container_groups.create_or_update(rg_name, app_name, updated_container_group)

            print(f"Container App {app_name} updated with new image: {new_image_url}")
            return redeployed_app
        else:
            print(f"Container App {app_name} not found")
            return None