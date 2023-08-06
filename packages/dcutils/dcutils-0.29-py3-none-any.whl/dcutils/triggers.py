import logging
import datetime

def newly_uploaded_blobs(
    STORAGE_CLIENT,
    SRC_BUCKET,
    DEST_BUCKET,
    PARENT_FOLDER,
    depth 
):
    logging.info('NEWLY UPLOADED BLOBS')
    logging.info('SOURCE BUCKET: {}'.format(SRC_BUCKET))
    logging.info('DEST_BUCKET: {}'.format(DEST_BUCKET))
    logging.info('TIMESTAMP: {}'.format(datetime.datetime.now()))
    
    current_blobs_itr = STORAGE_CLIENT.list_blobs(DEST_BUCKET)
    src_blobs = STORAGE_CLIENT.list_blobs(SRC_BUCKET)
    new_blobs = []
    current_blobs = []
    
    for blob in current_blobs_itr:
        current_blobs.append(blob.name)

    for blob in src_blobs:
        folders = blob.name.split('/')
        if PARENT_FOLDER in folders[depth]:
            if blob.name not in current_blobs:
                new_blobs.append(blob)
                logging.info('{}'.format(blob.name))
    if len(new_blobs) == 0:
        logging.info('{} is updated with respect to {}'.format(DEST_BUCKET, SRC_BUCKET))
    return new_blobs