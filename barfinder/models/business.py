"""Models to handle businesses."""
import datetime as dt

from sqlalchemy.dialects.postgresql import JSONB

from barfinder.database import (Column, SurrogatePK, Model, db, relationship)


class Business(Model, SurrogatePK):
    """A business, either restaurant or bar."""
    __tablename__ = 'business'

    raw_yelp_data = Column(JSONB)
    yelp_id = Column(db.String(255), index=True, nullable=True, unique=True)
    name = Column(db.String(255), nullable=False, index=True)
    source = Column(db.String(255))
    price = Column(db.Integer(), index=True)
    latitude = Column(db.Float())
    longitude = Column(db.Float())
    phone = Column(db.String(50))
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    business_tags = relationship('BusinessTag', cascade='delete')


class Tag(Model, SurrogatePK):
    """A tag associated with a business."""
    __tablename__ = 'tag'

    title = Column(db.String(255))
    alias = Column(db.String(255), index=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    business_tags = relationship('BusinessTag', cascade='delete')


class BusinessTag(Model):
    """A join table for a Business <-> Tag relation."""
    __tablename__ = 'business_tag'

    business_id = Column(db.ForeignKey('business.id', ondelete='CASCADE'),
                         primary_key=True)
    business = relationship('Business')
    tag_id = Column(db.ForeignKey('tag.id', ondelete='CASCADE'),
                    primary_key=True)
    tag = relationship('Tag')
