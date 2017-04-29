import os


KEY_VAR = 'YELP_KEY'
YELP_KEY = os.environ.get(KEY_VAR)


def lambda_crawl(event, context):
    if not YELP_KEY:
        raise RuntimeError('No API keys specified. Assign keys to the'
                           ' environment variable: {}'.format(KEY_VAR))
    from crawl import crawl_businesses
    crawl_businesses(key=YELP_KEY)
