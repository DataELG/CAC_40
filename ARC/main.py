# Load libraries
from azure.storage.blob import BlobClient
import pandas as pd

# Define parameters
connectionString = "DefaultEndpointsProtocol=https;AccountName=comptestockagetest;AccountKey=mJwmGf2WnTfyuHgzkvXD0n2hfA4moYann2pMeVsPoPJCYkp8GWTH25YZ9KYuSZFjE/6K/1U/1c8Y+AStwNA66g==;EndpointSuffix=core.windows.net"
containerName = "output"
outputBlobName	= "iris_setosa.csv"

# Establish connection with the blob storage account
blob = BlobClient.from_connection_string(conn_str=connectionString, container_name=containerName, blob_name=outputBlobName)

# Load iris dataset from the task node
df = pd.read_csv("iris.csv")

# Take a subset of the records
df = df[df['Species'] == "setosa"]

# Save the subset of the iris dataframe locally in the task node
df.to_csv(outputBlobName, index = False)

with open(outputBlobName, "w+b") as data:
    blob.upload_blob(data, overwrite=True)