from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleAssignmentCreateParameters, PrincipalType
import uuid

class AuthManagement:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.AZURE_SUBSCRIPTION_ID = AZURE_SUBSCRIPTION_ID
        self.client = AuthorizationManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    def authAccessToACR(self, identity_principal_id , acr_name, acr_rg_name):
        # Scope for ACR
        acr_scope = f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{acr_rg_name}/providers/Microsoft.ContainerRegistry/registries/{acr_name}"

        role_assignment_params = RoleAssignmentCreateParameters(
            role_definition_id = f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/providers/Microsoft.Authorization/roleDefinitions/7f951dda-4ed3-4680-a7ca-43fe172d538d",  # AcrPull role ID
            principal_id = identity_principal_id,
            principal_type = PrincipalType.SERVICE_PRINCIPAL  # <--- important!
        )

        assignment_name = str(uuid.uuid4())

        self.client.role_assignments.create(
            scope=acr_scope,
            role_assignment_name=assignment_name,
            parameters=role_assignment_params
        )

    def authAccessToRG(self, identity_principal_id, rg_name):
        # Scope: Resource Group level
        scope = f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{rg_name}"

        role_assignment_params = RoleAssignmentCreateParameters(
            principal_id=identity_principal_id,
            role_definition_id=f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/providers/Microsoft.Authorization/roleDefinitions/acdd72a7-3385-48ef-bd42-f606fba81ae7",  # Reader role
            principal_type=PrincipalType.SERVICE_PRINCIPAL
        )

        self.client.role_assignments.create(
            scope=scope,
            role_assignment_name=str(uuid.uuid4()),
            parameters=role_assignment_params
        )

    def authAccessToStorage(self, identity_principal_id, rg_name, storage_account_name):
        # Scope: Resource Group level
        scope = f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}"

        role_assignment_params = RoleAssignmentCreateParameters(
            principal_id=identity_principal_id,
            role_definition_id=f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/providers/Microsoft.Authorization/roleDefinitions/ba92f5b4-2d11-453d-a403-e96b0029c9fe",  # "Storage Blob Data Contributor"
            principal_type="ServicePrincipal"
        )

        self.client.role_assignments.create(
            scope=scope,
            role_assignment_name=str(uuid.uuid4()),
            parameters=role_assignment_params
        )

