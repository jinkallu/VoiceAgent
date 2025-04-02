from azure.storage.blob import BlobServiceClient
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential
from azure.core.exceptions import ResourceExistsError, AzureError
import os
import json
from dotenv import load_dotenv


load_dotenv()

class BlobOps:
    def __init__(self):
        self.blob_service_client = None
        self.container_client = None
        self.blob_client = None

        

    def setBlobServiceClient(self, storage_name, credential=None):
        if not credential:
            credential = DefaultAzureCredential()
        connection_url = f"https://{storage_name}.blob.core.windows.net"

        # Create the BlobServiceClient object
        self.blob_service_client = BlobServiceClient(connection_url, credential=credential)

    def getContainersList(self):
        containers=self.blob_service_client.list_containers()
        print("containers",containers)
        return containers
    

    def setContainerClient(self, container_name):
        # Get a container client to interact with the container
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def getBlobData(self, blob_name):
        try:
            # Get a blob client to interact with the specific blob
            blob_client = self.container_client.get_blob_client(blob_name)
            print(blob_client.url)

            # Download the blob's content
            blob_data = blob_client.download_blob()
            content = blob_data.readall()  # Read the content as bytes
            
            # Optionally, you can decode the bytes into a string (if it's text data)
            #content_str = content.decode('utf-8')
        
            return content
        except Exception as e:
            print("Blob read error", blob_name)
    
    def getStorageMapping(self, mapping_blob_name):
        return self.getBlobData(mapping_blob_name)
    
    def getStorageMappingAsJson(self, mapping_blob_name):
        json_str = self.getStorageMapping(mapping_blob_name)
        return json.loads(json_str)
    
    def getProductData(self, product_blob_name):
        data = self.getBlobData(product_blob_name)
        return data
    
    def createContainerIfNotExists(self, container_name):
        container_client = self.blob_service_client.get_container_client(container_name)
        # Create container if it doesn't exist
        try:
            container_client.create_container()
            return True
        except Exception as e:
            print("Container may already exist:", e)

    def createOrUpdateBlob(self, blob_name, blob_bytes):
        blob_client = self.container_client.get_blob_client(blob_name)
        try:
            # Upload the JSON string
            blob_client.upload_blob(blob_bytes, overwrite=True)
            return True
        except AzureError as e:
            print(f"❌ Azure error occurred: {e}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    
    def createOrReplaceBlobFromJson(self, blob_name, json_data):
        self.createOrUpdateBlob(blob_name, json_data)
        

    def createOrReplaceBlobFromPyDict(self, blob_name, py_dict):
        # Convert to string or bytes
        json_string = json.dumps(py_dict)
        return self.createOrReplaceBlobFromJson(blob_name, json_string)










if __name__ == "__main__":
    blobOps = BlobOps()
    blobOps.setBlobServiceClient(storage_name="tralpinestorage1")
    blobOps.setContainerClient(os.environ.get("PRODUCTS_BLOB_CONTAINER"))
    print(blobOps.getStorageMappingAsJson(os.environ.get("MAPPING_BLOB")))
    json_data = {
        "name": "John",
        "age": 31,
        "city": "New York"
    }
    print(blobOps.createOrReplaceBlobFromPyDict("test1.json", json_data))
