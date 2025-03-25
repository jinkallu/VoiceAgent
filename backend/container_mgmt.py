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

class ContainerManagement:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.containerapp_client = ContainerAppsAPIClient(credential, AZURE_SUBSCRIPTION_ID)

    def getContainerAppURL(self, rg_name, app_name):
        app = self.containerapp_client.container_apps.get(rg_name, app_name)

        # Get the URL (Fully Qualified Domain Name)
        url = f"https://{app.configuration.ingress.fqdn}"
        print("Container App URL:", url)

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
    


