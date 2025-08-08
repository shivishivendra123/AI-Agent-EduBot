from google.cloud import storage
import uuid

def upload_to_gcs(bucket_name="assignment_agent", source_file_path='/Users/shivendragupta/Desktop/AI-Agent-Educational/homwork.pdf', destination_blob_name='Homework'):
    # Initialize a GCS client
    client = storage.Client()
    
    # Get the bucket
    bucket = client.bucket(bucket_name)
    
    # Create a blob object and upload the file
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    print(f"Uploaded {source_file_path} to gs://{bucket_name}/{destination_blob_name}")

# Example usage
upload_to_gcs()
