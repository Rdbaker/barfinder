"""Callbacks to handle facebook events."""
from sqlalchemy.dialects.postgresql import JSONB

from barfinder.database import Column, SurrogatePK, Model


class RawFBMessage(Model, SurrogatePK):
    """A raw message from facebook."""
    __tablename__ = 'raw_fb_message'
    message = Column(JSONB, nullable=False)


def receive_message(event):
    RawFBMessage.create(message=event.messaging)
    sender_id = event.sender_id
    message = event.message_text
    return sender_id, 'thanks for your message: {}'.format(message)
