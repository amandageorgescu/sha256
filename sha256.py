#!/usr/local/bin/env python

import flask
import flask_sqlalchemy
import hashlib
from flask import request, json
from flask import render_template
from flask import abort

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = flask_sqlalchemy.SQLAlchemy(app)

class Message(db.Model):
	__tablename__ = 'messages'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sha256 = db.Column(db.String(256))
	original_message = db.Column(db.String(256))

	def __init__(self, sha256=None, original_message=None):
		self.sha256 = sha256
		self.original_message = original_message

@app.route('/messages', methods = ['POST'])
def post_message():
	if request.method == 'POST':
		original_message = request.json['message']
		sha256 = hashlib.sha256(original_message).hexdigest()
		message = Message(sha256, original_message)
		db.session.add(message)
		db.session.commit()
		return json.dumps({"digest":sha256})

@app.route('/messages/<sha256>', methods = ['GET'])
def get_message(sha256):
	message = Message.query.filter(Message.sha256 == sha256).first()
	if message != None:
		return json.dumps({"message":message.original_message})
	else:
		abort(404)

if __name__ == '__main__':
	db.create_all()
	app.run()

