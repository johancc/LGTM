from google.cloud import storage
import os

client = storage.Client()
bucket = client.get_bucket('ethan_garza_first_bucket')

overall_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_sound_file.wav")

def upload(file):
    blob = bucket.blob(file)
    blob.upload_from_string('this is test content!')

def make_blob_public(bucket_name, blob_name):
    """Makes a blob publicly accessible."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.make_public()

    print('Blob {} is publicly accessible at {}'.format(
        blob.name, blob.public_url))

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = "test_file"
    full_dir = os.path.join(dir_path, filename + ".m4a")
    upload_blob('ethan_garza_first_bucket', full_dir, "test_file.m4a")
