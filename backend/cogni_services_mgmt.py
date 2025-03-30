from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.cognitiveservices.models import Sku, Account, AccountProperties, ApiProperties, DeploymentProperties, DeploymentModel , Deployment, DeploymentScaleSettings, DeploymentCapacitySettings 
from pprint import pprint

class CognitiveServicesMgmt:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.client = CognitiveServicesManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    def createServiceResource(self, rg_name, account_name, location):
        account = Account(
            location=location,
            sku=Sku(name="S0"),
            kind="OpenAI",  # other options: "CognitiveServices", "TextAnalytics", etc.
            properties={}
        )

        try:
            poller =self.client.accounts.begin_create(
                resource_group_name=rg_name,
                account_name=account_name,
                account=account
            )

            account = poller.result()
            print(f"Created Cognitive Services account: {account.name} in {account.location}")
            return account
        except Exception as e:
            print(f"Error in Creation of Cognitive Services account: {account_name} in {location} {e}")

    def getDeployment(self, rg_name, account_name, deployment_name):
        try:
            deployment = self.client.deployments.get(rg_name, account_name, deployment_name)
            return deployment
        except Exception as e:
            print(f"No deployment {deployment_name}", e)


    def createDeployment(self, rg_name, account_name, location, deployment_name, model_name, version, capacity=10):
        # Define the deployment configuration
        deployment = Deployment(
            sku=Sku(
                    name="GlobalStandard",
                    capacity=capacity, # 440 000 Tokens per minute, 2640 request per minute
                    
                ),  # You can adjust the SKU as needed
            properties=DeploymentProperties(
                model=DeploymentModel (
                    format="OpenAI",
                    name=model_name,  # Specify the model name (you may need to specify the model version if needed)
                    version= version # Specify the version of the model
                ),
                current_capacity=1,  # Set the desired capacity for deployment,
            )
        )

        # Begin the creation or update process of the deployment
        try:
            poller = self.client.deployments.begin_create_or_update(
                resource_group_name=rg_name,
                account_name=account_name,
                deployment_name=deployment_name,
                deployment=deployment
            )

            deployment_result = poller.result()  # Get the result of the deployment creation
            print(f"Deployment created/updated: {deployment_result.name}")
            return deployment_result
        except Exception as e:
            print(f"Error in deployment creation: {str(e)}")


    def getAIService(self, rg_name, account_name):
        try:
            account = self.client.accounts.get(rg_name, account_name)
            return account
        
        except Exception as e:
            print("Could not get teh AI service", e )


    

