from azure.storage.blob import BlobServiceClient
from azure.identity import AzureDeveloperCliCredential, DefaultAzureCredential
import os
import json
from dotenv import load_dotenv



class BlobOps:
    def __init__(self):
        self.blob_service_client = None
        self.container_client = None
        self.blob_client = None

        if not os.environ.get("PRODUCTS_BLOB_CONTAINER"):
            load_dotenv()
        

    def setBlobServiceClient(self, storage_name):
        default_credential = DefaultAzureCredential()
        connection_url = f"https://{storage_name}.blob.core.windows.net"

        # Create the BlobServiceClient object
        self.blob_service_client = BlobServiceClient(connection_url, credential=default_credential)

    def setContainerClient(self, container_name):
        # Get a container client to interact with the container
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def getBlobData(self, blob_name):
        # Get a blob client to interact with the specific blob
        blob_client = self.container_client.get_blob_client(blob_name)

        # Download the blob's content
        blob_data = blob_client.download_blob()
        content = blob_data.readall()  # Read the content as bytes
        
        # Optionally, you can decode the bytes into a string (if it's text data)
        content_str = content.decode('utf-8')
        
        return content_str
    
    def getStorageMapping(self, mapping_blob_name):
        return self.getBlobData(mapping_blob_name)
    
    def getStorageMappingAsJson(self, mapping_blob_name):
        json_str = self.getStorageMapping(mapping_blob_name)
        return json.loads(json_str)





if __name__ == "__main__":
    blobOps = BlobOps()
    blobOps.setBlobServiceClient(storage_name="tralpinestorage1")
    blobOps.setContainerClient(os.environ.get("PRODUCTS_BLOB_CONTAINER"))
    print(blobOps.getStorageMappingAsJson(os.environ.get("MAPPING_BLOB")))
