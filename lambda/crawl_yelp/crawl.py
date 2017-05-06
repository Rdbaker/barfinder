import json
import logging
import os

import boto3
import requests

logging.getLogger().setLevel(logging.INFO)

# 10 miles * 1000 meters/km * 1.6 km/mi
RADIUS = os.environ.get('RADIUS') or int(10 * 1000 * 1.6)
LAT = os.environ.get('LAT') or 42.3542685
LON = os.environ.get('LON') or -71.0694473
PER_PAGE = os.environ.get('PER_PAGE') or 20
YELP_URL = 'https://api.yelp.com/v3/businesses/search'
KINESIS_STREAM = os.environ.get('KINESIS_STREAM') or 'yelp-restaurant-ingest'
OFFSET = os.environ.get('OFFSET') or 0


def get_auth_header(key):
    """Return the authorization headers for the eventbrite request."""
    return {'Authorization': 'Bearer {}'.format(key)}


def get_paginated_businesses(offset=OFFSET, key=None, radius=RADIUS, lat=LAT,
                             lon=LON):
    """Get the businesses <radius> distance from <lat>,<lon>"""
    res = requests.get(
        YELP_URL,
        params={'radius': radius,
                'latitude': lat,
                'longitude': lon,
                'categories': 'bars,restaurants',
                'limit': PER_PAGE,
                'offset': offset},
        headers=get_auth_header(key))
    if res.status_code >= 400:
        logging.warning('got a bad response from yelp, bailing')
        logging.warning(res.status_code)
        logging.warning(res.text)
        return None, None
    else:
        return res, offset + PER_PAGE


def send_businesses_to_stream(businesses):
    client = boto3.client('lambda')
    for business in businesses:
        client.invoke_async(FunctionName='yelp-restaurant-extract',
            InvokeArgs=json.dumps(business))
        logging.info('successfully sent business ({}) to lambda function'
            .format(business['id']))


def crawl_businesses(key, radius=RADIUS, lat=LAT, lon=LON):
    """Get the Yelp businesses within RADIUS of LAT:LON."""
    response, offset = get_paginated_businesses(key=key, lat=lat, lon=lon,
                                                radius=radius)
    total_businesses = response.json()['total']
    logging.info('processing businesses 1 through {}'.format(PER_PAGE))
    send_businesses_to_stream(response.json()['businesses'])
    while offset + PER_PAGE < total_businesses:
        logging.info('processing businesses {} through {}'
                     .format(offset, offset + PER_PAGE))

        response, offset = get_paginated_businesses(offset=offset, key=key,
                                                    lat=lat, lon=lon,
                                                    radius=radius)
        if response is not None:
            send_businesses_to_stream(response.json()['businesses'])
        else:
            return 'Done'
