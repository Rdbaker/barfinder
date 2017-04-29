# -*- coding: utf-8 -*-
"""Location models."""
import datetime

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import (Table, Column, String, MetaData, DateTime,
                        Integer, Float, ForeignKey)


metadata = MetaData()


tag = Table(
    'tag',
    metadata,
    Column('id', Integer()),
    Column('title', String(255)),
    Column('alias', String(255)),
    Column('created_at', DateTime(), default=datetime.datetime.utcnow),
)


business_tag_join_table = Table('business_tag', metadata,
                                Column('tag_id', Integer,
                                       ForeignKey('tag.id', ondelete='DELETE')),
                                Column('business_id', Integer,
                                       ForeignKey('business.id',
                                                  ondelete='DELETE')))


business = Table(
    'business',
    metadata,
    Column('id', Integer()),
    Column('raw_yelp_data', JSONB()),
    Column('yelp_id', String(255)),
    Column('name', String(255)),
    Column('source', String(255)),
    Column('price', Integer()),
    Column('latitude', Float()),
    Column('longitude', Float()),
    Column('phone', String(50)),
    Column('created_at', DateTime(), default=datetime.datetime.utcnow),
)
