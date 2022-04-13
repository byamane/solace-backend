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
@login_required
def index():
  profile = read_token(request)
  prof_id = profile['id']
  # print(f'PROFILE id, {prof_id}')
  # sleepLogs = Sleep.query.all()
  sleepLogs = Sleep.query.filter_by(profile_id=prof_id).all()
  # print(f'SLEEPLOGS, {sleepLogs}')
  return jsonify([sleep.serialize() for sleep in sleepLogs]), 200

@sleepLogs.route('/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  sleep = Sleep.query.filter_by(id=id).first()

  if sleep.profile_id != profile['id']:
    return 'Forbidden', 403
  
  for key in data:
    setattr(sleep, key, data[key])
  
  db.session.commit()
  return jsonify(sleep.serialize()), 200


@sleepLogs.route('/<id>', methods=['DELETE'])
@login_required
def delete(id):
  profile = read_token(request)
  sleep = Sleep.query.filter_by(id=id).first()

  if sleep.profile_id != profile['id']:
    return 'Forbidden', 403
  
  db.session.delete(sleep)
  db.session.commit()
  return jsonify(message='Success'), 200