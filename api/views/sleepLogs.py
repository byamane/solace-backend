from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.sleep import Sleep

sleepLogs = Blueprint('sleepLogs', 'sleepLogs')

@sleepLogs.route('/', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data['profile_id'] = profile['id']
  sleep = Sleep(**data)
  db.session.add(sleep)
  db.session.commit()
  return jsonify(sleep.serialize()), 201

@sleepLogs.route('/', methods=['GET'])
def index():
  sleepLogs = Sleep.query.all()
  return jsonify([sleep.serialize() for sleep in sleepLogs]), 200