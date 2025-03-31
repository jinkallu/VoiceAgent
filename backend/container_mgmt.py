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
    EnvironmentVar
)
from azure.core.exceptions import ResourceNotFoundError

class ContainerManagement:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.containerapp_client = ContainerAppsAPIClient(credential, AZURE_SUBSCRIPTION_ID)

    def getContainerAppURL(self, rg_name, app_name):
        app = self.containerapp_client.container_apps.get(rg_name, app_name)

        # Get the URL (Fully Qualified Domain Name)
        url = f"https://{app.configuration.ingress.fqdn}"
        print("Container App URL:", url)

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


    


