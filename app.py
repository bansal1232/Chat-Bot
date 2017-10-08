import os, sys

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200
	
@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	return "ok", 200

def log(message):
	print(message)
	sys.stdout.flush()
if __name__ == "__main__":
 app.run(debug = True, port=80)
