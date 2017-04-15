import json
import os

from flask import Blueprint, request, current_app, jsonify

from barfinder.extensions import csrf_protect

mod = Blueprint('chat', __name__, url_prefix='/api/chat')


@mod.route('/messages', methods=['GET'])
def getmessages():
    return '', 200


@mod.route('/messages', methods=['POST'])
@csrf_protect.exempt
def createmessage():
    message = request.get_json()['body']
    ai_req = current_app.api_ai.text_request()
    ai_req.session_id = '1'
    ai_req.query = message
    ai_res = ai_req.getresponse()
    return jsonify(json.loads(ai_res.read())), 200


@mod.route('/messages/facebook', methods=['POST'])
@csrf_protect.exempt
def receive_fb_message():
    return 'hi!', 200


@mod.route('/messages/facebook', methods=['GET'])
def verify_fb_callback():
    challenge = request.args.get('hub.challenge')
    verify_token = request.args.get('hub.verify_token')
    if verify_token == os.environ.get('FB_VERIFY_TOKEN'):
        return challenge, 200
    else:
        return 'forbidden', 403
