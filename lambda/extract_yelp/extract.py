import logging

from models import tag as Tag, business as Business, business_tag_join_table

logging.getLogger().setLevel(logging.INFO)


def parse_yelp_business(business):
    return {
        'source': 'yelp',
        'raw_yelp_data': business,
        'yelp_id': business.get('id'),
        'name': business.get('name', 'UNKNOWN'),
        'price': len(business.get('price', '')),
        'latitude': business.get('coordinates', {}).get('latitude'),
        'longitude': business.get('coordinates', {}).get('longitude'),
        'phone': business.get('phone'),
    }


def business_exists(yelp_id, conn):
    """Return True if the business exists."""
    return conn.execute(Business.select().where(Business.c.yelp_id == yelp_id))\
        .first() is not None


def delete_business(yelp_id, conn):
    """Delete the business with the given yelp id."""
    return conn.execute(Business.delete().where(Business.c.yelp_id == yelp_id))


def tag_exists(alias, conn):
    return conn.execute(Tag.select().where(Tag.c.alias == alias))\
        .first() is not None


def create_tag(tag, conn):
    conn.execute(Tag.insert().values(**tag))


def get_or_create_tags(tags, conn):
    names = []
    for tag in tags:
        if not tag_exists(tag['alias'], conn):
            create_tag(tag, conn)
        names.append(tag['alias'])
    return conn.execute(Tag.select().where(Tag.c.alias.in_(names))).fetchall()


def create_business(business, conn):
    conn.execute(Business.insert().values(**business))
    return conn.execute(Business.select().where(Business.c.yelp_id ==
                                                business['yelp_id'])).first()


def link_business_to_tags(business, tags, conn):
    for tag in tags:
        conn.execute(
            business_tag_join_table.insert().values(tag_id=tag.id,
                                                    business_id=business.id))


def extract_business(business_dict, engine):
    conn = engine.connect()
    if business_exists(business_dict['id'], conn):
        delete_business(business_dict['id'], conn)
    business = parse_yelp_business(business_dict)
    tags = get_or_create_tags(business_dict['categories'], conn)
    business = create_business(business, conn)
    link_business_to_tags(business, tags, conn)
    logging.info('successfully processed business: {}'
                 .format(business_dict['id']))
