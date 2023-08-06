from tenacity import retry, wait_fixed, stop_after_attempt
from requests.utils import quote
from google.cloud import storage
import requests
import time
import logging
import datetime

@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def cp_batch(
    STORAGE_CLIENT,
    SRC_BUCKET,
    DEST_BLOB,
    DEST_BUCKET,
    PARENT_FOLDER,
    depth,
    access_token
):
    filehandler = logging.FileHandler('/tmp/process.log'.format(datetime.datetime.now()))
    filehandler.setLevel(logging.INFO)

    if (logging.hasHandlers()):
        logging.handlers.clear()
    logging.info('START Timestamp: {}'.format(datetime.datetime.now()))

    blobs = STORAGE_CLIENT.list_blobs(SRC_BUCKET)
    for blob in blobs:
        try:
            folders = blob.name.split('/')
            if PARENT_FOLDER in folders[depth]:
                cp_blob(
                    STORAGE_CLIENT,
                    blob.name,
                    DEST_BLOB + '/' + blob.name,
                    SRC_BUCKET,
                    DEST_BUCKET,
                    access_token
                    )
        except Exception as e:
            print('Error: {}'.format(e))
            logging.info('Error: {}'.format(e))
            
#@retry(wait=wait_fixed(2), stop=stop_after_attempt(3))
def cp_blob(
    STORAGE_CLIENT,
    blob_name,
    new_blob_name,
    bucket_name,
    new_bucket_name,
    access_token
    ):
    filehandler = logging.FileHandler('/tmp/process.log'.format(datetime.datetime.now()))
    filehandler.setLevel(logging.INFO)

    if (logging.hasHandlers()):
        logging.handlers.clear()

    logging.addHandler(filehandler)
    logging.info('START Timestamp: {}'.format(datetime.datetime.now()))

    source_bucket = STORAGE_CLIENT.get_bucket(bucket_name)
    source_blob = source_bucket.get_blob(blob_name)
    destination_bucket = STORAGE_CLIENT.get_bucket(new_bucket_name)
    
    time.sleep(0.05)

    # get size of blob
    blob_size = source_blob.size

    # rewrite of blob greater than 15mb
    if (blob_size > 15000000):
        source_bucket_url = quote(source_bucket.name, safe='')
        source_blob_url = quote(source_blob.name, safe='')
        destination_bucket_url = quote(destination_bucket.name, safe='')
        new_blob_name = quote(new_blob_name, safe = '')
        url = "https://storage.googleapis.com/storage/v1/b/{}/o/{}/rewriteTo/b/{}/o/{}".format(
                    source_bucket_url, 
                    source_blob_url,
                    destination_bucket_url,
                    new_blob_name)
        try:
            response = requests.post(url, headers = access_token)
            logging.info('rewriting {} to {}\n'.format(source_blob.name, new_blob_name))
            print('rewriting {} to {}\n'.format(source_blob.name, new_blob_name))
            if ('done' not in response.json()):
                logging.info('rewrite operation failed with the following error: {}'.format(response.text))
                print('rewrite operation failed with the following error: {}'.format(response.text))
            else:
                logging.info('rewrite operation successful!')
                print('rewrite operation successful!')
        except Exception as e:
            logging.info('Error: {}'.format(e))
            print('Error: {}'.format(e))
    else:
        #copy to new destination
        logging.info('copied {} to {}\n'.format(source_blob.name, new_blob_name))
        print('copied {} to {}\n'.format(source_blob.name, new_blob_name))            