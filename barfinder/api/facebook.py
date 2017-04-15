"""Callbacks to handle facebook events."""


def receive_message(event):
    sender_id = event.sender_id
    message = event.message_text
    return sender_id, 'thanks for your message: {}'.format(message)
