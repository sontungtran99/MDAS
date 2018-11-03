from flask import Flask, request
import data.init_users


app = Flask(__name__)


@app.route('/response', methods=['POST'])
def receive_SMS():
	# Receives SMS from users who wants to register to use the service
	sms = request.get_json()
	phonenum, message = sms['phone'], sms['content']
	init_users(phonenum, message)
	print('Received message of {}, location: {}'.format(phonenum, message))
	return None

if __name__ == '__main__':
	app.run(debug=True)

