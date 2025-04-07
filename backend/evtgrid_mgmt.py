from azure.mgmt.eventgrid import EventGridManagementClient
from azure.mgmt.eventgrid.models import EventSubscription, WebHookEventSubscriptionDestination, EventSubscriptionFilter

class EventGridMgmt:
    def __init__(self, credential, AZURE_SUBSCRIPTION_ID):
        self.AZURE_SUBSCRIPTION_ID = AZURE_SUBSCRIPTION_ID
        self.client = EventGridManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    def createBlobStorageEvtSubscription(self, rg_name, storage_account_name, container_app_url, event_subscription_name):
        # Get the Storage Account resource ID
        storage_account_id = f"/subscriptions/{self.AZURE_SUBSCRIPTION_ID}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}"

        # Create EventSubscriptionFilter for event types
        event_filter = EventSubscriptionFilter(
            included_event_types=["Microsoft.Storage.BlobCreated", "Microsoft.Storage.BlobDeleted"]
        )
        # Create the Event Subscription
        event_subscription = EventSubscription(
            destination=WebHookEventSubscriptionDestination(
                endpoint_url=container_app_url
            ),
            filter=event_filter,  # You can specify filters (optional)
            event_delivery_schema="EventGridSchema",  # The schema format for the event
        )

        # Create the event subscription
        try:
            poller = self.client.event_subscriptions.begin_create_or_update(
                #resource_group_name=rg_name,
                event_subscription_name=event_subscription_name,
                scope=storage_account_id,
                event_subscription_info=event_subscription
            )

            evt = poller.result()

            print(f"Event Subscription '{event_subscription_name}' created successfully!", evt)
            return True
        except Exception as e:
            print(e)
            return False
