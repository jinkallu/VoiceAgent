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
