import json

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
