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

    def createContainerEnv(self, rg_name, env_name, location):
        # Define the environment
        env = ManagedEnvironment(
            location=location,
            app_logs_configuration=AppLogsConfiguration(
                destination="log-analytics",
                log_analytics_configuration=LogAnalyticsConfiguration(
                    customer_id="ca1b0560-7f1c-4eea-a6da-b968bdd0b0c4",
                    shared_key="KA0BmejW7tnAfCRsjSAH4SdsNzQGuYiA638JAKfelG5rQTypDlZWsVC5dzAW81JMEITVJ14kaEJCdp1mVaT87A=="
                )
            ),
            tags={"env": "dev"}  # optional tags
        )

        # Create or update the environment
        poller = self.containerapp_client.managed_environments.begin_create_or_update(
            resource_group_name=rg_name,
            environment_name=env_name,
            environment_envelope=env
        )

        result = poller.result()
        print(f"✅ Container App Environment created: {result.name}")

    


