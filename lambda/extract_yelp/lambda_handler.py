import base64
import json
import logging
import os

from sqlalchemy import create_engine

from extract import extract_business

logging.getLogger().setLevel(logging.INFO)


DATABASE_URI = os.environ.get('DATABASE_URI')
ENGINE = create_engine('postgres://' + DATABASE_URI,
                       connect_args={'sslmode': 'require'})


def lambda_extract(event, context):
    if not DATABASE_URI:
        raise RuntimeError('No DATABASE_URI was supplied')
    try:
        business = json.loads(event)
    except:
        logging.warning('could not load JSON from data: {}'.format(event))

    try:
        extract_business(business_dict=business, engine=ENGINE)
    except:
        logging.warning('could not extract business from dict: {}'
                        .format(business))
        raise
