from azure.mgmt.appcontainers import ContainerAppsAPIClient
from azure.mgmt.appcontainers.models import (
    ManagedEnvironment,
    AppLogsConfiguration,
    LogAnalyticsConfiguration,
    ContainerApp,
    Ingress,
    Configuration,
    Template,
    Container,
    ContainerResources,
    EnvironmentVar,
    ManagedServiceIdentity, ManagedServiceIdentityType
)
from azure.core.exceptions import ResourceNotFoundError

class ContainerAppManagement:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.AZURE_SUBSCRIPTION_ID = AZURE_SUBSCRIPTION_ID
        self.containerapp_client = ContainerAppsAPIClient(credential, AZURE_SUBSCRIPTION_ID)

    def getContainerAppURL(self, rg_name, app_name):
        app = self.containerapp_client.container_apps.get(rg_name, app_name)

        # Get the URL (Fully Qualified Domain Name)
        url = f"https://{app.configuration.ingress.fqdn}"
        print("Container App URL:", url)
        return url

    def getContainerAppsEnv(self, rg_name, env_name):
        try:
            container_apps_env = self.containerapp_client.managed_environments.get(rg_name, env_name)
            return container_apps_env
        except ResourceNotFoundError:
            print(f"Container App '{env_name}' does not exist.")

    def createContainerEnv(self, rg_name, env_name, location, customer_id, shared_key):
        # Define the environment
        env = ManagedEnvironment(
            location=location,
            app_logs_configuration=AppLogsConfiguration(
                destination="log-analytics",
                log_analytics_configuration=LogAnalyticsConfiguration(
                    customer_id=customer_id,
                    shared_key=shared_key
                )
            ),
            tags={"env": "dev"}  # optional tags
        )

        # Create or update the environment
        try:
            poller = self.containerapp_client.managed_environments.begin_create_or_update(
                resource_group_name=rg_name,
                environment_name=env_name,
                environment_envelope=env
            )

            result = poller.result()
            return result
        except Exception as e:
            print(f"Workspace creation failed: {e}")

    def getContainerApp(self, rg_name, app_name):
        try:
            container_apps = self.containerapp_client.container_apps.get(rg_name, app_name)
            return container_apps
        except ResourceNotFoundError:
            print(f"Container App '{app_name}' does not exist.")

    def createContainerApp(self, subscription_id, rg_name, env_name, app_name, location):

        # Define the container app
        container_app = ContainerApp(
            location=location,  # or your preferred region
            environment_id=f"/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.App/managedEnvironments/{env_name}",
            template=Template(
                containers=[
                    Container(
                        name="mycontainer",
                        image="nginx:latest",  # your container image
                        env=[
                            EnvironmentVar(name="ENV_VAR_EXAMPLE", value="value")
                        ],
                    )
                ],
                scale={"min_replicas": 1, "max_replicas": 2}
            ),
            configuration={
                "ingress": Ingress(
                    external=True,
                    target_port=80,
                ),
                "active_revisions_mode": "Single",
            },
            tags={
                "env": "dev"
            }
        )

        try:
            poller = self.containerapp_client.container_apps.begin_create_or_update(
                resource_group_name=rg_name,
                container_app_name=app_name,
                container_app_envelope=container_app
            )
            result = poller.result()  # Wait for deployment to complete
            return result
        except ResourceNotFoundError:
            print(f"Container App '{app_name}' creation failed.")


    def assign_identity_to_containerapp(self, rg_name, container_app_name, identity_name):
        """
        Assigns a User-Assigned Managed Identity to an Azure Container App
        """
        print(f"Assigning Managed Identity {identity_name} to Container App {container_app_name} in {rg_name}...")

        # Get the existing container app configuration
        container_app = self.containerapp_client.container_apps.get(rg_name, container_app_name)

        # Attach the identity
        identity_scope = f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identity_name}"
        container_app.identity = ManagedServiceIdentity(
            type=ManagedServiceIdentityType.USER_ASSIGNED,
            user_assigned_identities={identity_scope: {}}
        )

        # Update the container app with identity
        update_operation = self.containerapp_client.container_apps.begin_update(rg_name, container_app_name, container_app)
        update_operation.wait()

        print(f"✅ Managed Identity {identity_name} assigned to Container App {container_app_name}!")



    def updateContainerApp(self, rg_name, app_name, new_acr_name, new_image_name, new_image_tag, location, environment_name, identity_name, e_vars):
        # Step 2: Get the existing container app
        existing_app = self.containerapp_client.container_apps.get(rg_name, app_name)

        if existing_app:
            # Step 3: Update the image URL
            new_image_url = f"{new_acr_name}.azurecr.io/{new_image_name}:{new_image_tag}"

            # Define the environment variables to pass to your container
            env_vars = []
            for var in e_vars:
                env_vars.append(
                    EnvironmentVar(
                        name=var["name"],  # The name of the environment variable
                        value=var["value"]  # The value of the environment variable
                    )
                )


            # Step 4: Update the container app's configuration with the new image
            # Prepare the containers configuration
            containers = [Container(
                name=existing_app.name,  # Keep the same name
                image=new_image_url,  # Set the new image URL
                resources=existing_app.template.containers[0].resources,  # Keep the same resources
                env=env_vars  # Pass environment variables here
            )]

            # Define the registry information (ACR)
            registries = [
                {
                    "server": f"{new_acr_name}.azurecr.io",  # ACR server address
                    "username": "",  # Leave empty if using Managed Identity
                    "passwordSecretRef": "",  # Can provide secret reference if necessary
                    "identity": f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identity_name}"
                }
            ]

            # Define Managed Identity
            managed_identity = ManagedServiceIdentity(
                type="UserAssigned",
                user_assigned_identities={
                    f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identity_name}": {}
                }
            )

            # Define the template for the container app
            container_app_template = Template(
                containers=containers
            )
            # Define the container app configuration, including the registry
            configuration = Configuration(
                registries=registries  # Add registry configuration to the container app configuration
            )

            environment_id = f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{rg_name}/providers/Microsoft.App/managedEnvironments/{environment_name}"

            # Step 4: Create the ContainerApp object
            container_app_envelope = ContainerApp(
                location=location,  # Ensure location is included
                identity=managed_identity,  # Managed identity for the app
                environment_id=environment_id,  # The environment ID
                template=container_app_template,  # Container template
                configuration=configuration,  # Add configuration with registries
            )

            # Step 5: Update the container app
            redeployed_app = self.containerapp_client.container_apps.begin_create_or_update(rg_name, app_name, container_app_envelope)
            redeployed_app.wait()

            print(f"Container App {app_name} updated with new image: {new_image_url}")
            return redeployed_app.result()  # This will wait until the update is complete
        else:
            print(f"Container App {app_name} not found")
            return None
