"""Callbacks to handle facebook events."""
import json

from fbmq import payload
from flask import current_app
from sqlalchemy.dialects.postgresql import JSONB

from barfinder.database import Column, SurrogatePK, Model

old_to_json = payload.utils.to_json


def del_none(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively.

    This alters the input so you may wish to ``copy`` the dict first.
    """
    # d.iteritems isn't used as you can't del or the iterator breaks.
    for key, value in d.items():
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d  # For convenience


def new_to_json(obj):
    new_obj = json.loads(json.dumps(obj, default=lambda o: o.__dict__,
                                    sort_keys=True))
    new_obj = del_none(new_obj)
    return json.dumps(new_obj, sort_keys=True)


payload.utils.to_json = new_to_json


class RawFBMessage(Model, SurrogatePK):
    """A raw message from facebook."""
    __tablename__ = 'raw_fb_message'
    message = Column(JSONB, nullable=False)


def receive_message(event):
    RawFBMessage.create(message=event.messaging)
    sender_id = event.sender_id
    message = event.message_text
    ai_req = current_app.api_ai.text_request()
    ai_req.query = message
    ai_req.session_id = sender_id
    ai_res = json.loads(ai_req.getresponse().read())
    ai_text = ai_res.get('result', {}).get('fulfillment', {})\
        .get('speech', '/shrug')
    return sender_id, ai_text
