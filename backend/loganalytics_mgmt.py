from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.loganalytics.models import Workspace

class LogAnalyticsMgmt:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.loanalytics_client = LogAnalyticsManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    def createWorkSpace(self, rg_name, workspace_name, location, sku={"name": "PerGB2018"}, retention_in_days=30):
        # Define workspace
        workspace_params = Workspace(
            location=location,
            sku={"name": "PerGB2018"},
            retention_in_days=30  # optional
        )

        # Create or update workspace
        try:
            poller = self.loanalytics_client.workspaces.begin_create_or_update(
                resource_group_name=rg_name,
                workspace_name=workspace_name,
                parameters=workspace_params
            )
            workspace = poller.result()
            return workspace

        except Exception as e:
            print(f"Workspace creation failed: {e}")

    def getSharedKeys(self, rg_name, workspace_name):
        shared_keys = self.loanalytics_client.shared_keys.get_shared_keys(
            resource_group_name=rg_name,
            workspace_name=workspace_name
        )

        return shared_keys.primary_shared_key
    # tests
    def test_create_loganalytics_workspace(self):
        self.createWorkSpace("test", "test-log-analytics", "westeurope")

    def test_getSharedKeys(self, rg_name, workspace_name):
        self.getSharedKeys(rg_name, workspace_name)
