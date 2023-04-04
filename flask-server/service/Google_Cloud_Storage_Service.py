from werkzeug.datastructures import FileStorage
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Meal_Model
class Google_Cloud_Storage_Service(object):
    def __init__(self) -> None:
        super().__init__()
        # Imports the Google Cloud client library
        from google.cloud import storage
        self.bucket_name = 'meal-photos'
        # Instantiates a client
        self.storage_client = storage.Client()

        self.bucket = self.storage_client.bucket(self.bucket_name)

    def create_bucket(self, bucket_name) -> None:
        # The name for the new bucket

        # Creates the new bucket
        bucket = self.storage_client.create_bucket(bucket_name)

        print('Bucket {} created.'.format(bucket.name))

    def upload_meal_image_file(self, meal: 'Meal_Model') ->'Meal_Model':
        '''Uploads a file to the bucket.'''
        # bucket_name = 'your-bucket-name'
        # file = 'local/path/to/file' this will be the business folder, with a folder named after the business' unique id, which will have the menu file in it
        # destination_blob_name = 'storage-object-name' this will be the business uuid
        # read an image
        with open(meal.image_url, 'rb') as file_bytes:
            file = FileStorage(file_bytes)
            file_type = meal.image_url.rsplit('.', 1)[1].lower()

            destination_blob_name = 'menu/' + \
                str(meal.id) + '.' + file_type
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_file(file)
            image_url_pre_fix = 'https://storage.googleapis.com/meal-photos/'
            image_url = image_url_pre_fix + destination_blob_name
            meal.image_url = image_url
            # blob.make_public()
            return meal
