from google.cloud import storage

def move_file_to_course_material(bucket_name, source_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Define the new destination path
    destination_blob_name = f"course_material/{source_file_name.split('/')[-1]}"

    source_blob = bucket.blob(source_file_name)

    # Copy the file to the new location
    bucket.copy_blob(source_blob, bucket, destination_blob_name)
    print(f"Copied to {destination_blob_name}")

    # Delete the original file
    source_blob.delete()
    print(f"Deleted original file {source_file_name}")

def upload_course_material_to_cloud(blob_name: str) -> str:
    # Example usage
    move_file_to_course_material(
        bucket_name="assignment_agent",
        source_file_name=blob_name
    )




