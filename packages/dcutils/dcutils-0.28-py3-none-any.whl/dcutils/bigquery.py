import datetime
import logging
from requests.utils import quote
from google.cloud import bigquery as bq
from google.api_core.exceptions import NotFound

def create_table(client, datasetId, name, schema):
    # clean datasetId
    datasetId = quote(datasetId, safe='')

    # initialize dataset and table reference
    ds_ref = client.dataset(datasetId)
    tb_ref = ds_ref.table(name)
    
    # create table if it does not exist
    try:
        client.get_table(tb_ref)
    except NotFound:
        table = bq.Table(tb_ref, schema=schema)
        table = client.create_table(table)
        logging.info('{}: CREATED TABLE {}'.format(datetime.datetime.now(), name))
        print('{}: CREATED TABLE {}'.format(datetime.datetime.now(), name))

def insert_row(BQ_client, table_id, row_array):
    table = BQ_client.get_table(table_id)
    errors = BQ_client.insert_rows(table, row_array)
    if errors == []:
        print('Row: {} has been added to table {}.'.format(row_array, table_id))