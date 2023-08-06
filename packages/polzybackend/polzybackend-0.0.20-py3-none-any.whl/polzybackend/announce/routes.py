from flask import Response
from datetime import date
from . import bp
from .. import messenger

@bp.route('/listen', methods=['GET'])
def listen():

    def stream():
        messages = messenger.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(
    	stream(),
    	headers={
    		"Access-Control-Allow-Origin": "*",
    		"Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
    	},
    	mimetype='text/event-stream',
    )