from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.journal import Journal

journalEntries = Blueprint('journalEntries', 'journalEntries')

@journalEntries.route('/', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  profile = read_token(request)
  data['profile_id'] = profile['id']
  journal = Journal(**data)
  db.session.add(journal)
  db.session.commit()
  return jsonify(journal.serialize()), 201

@journalEntries.route('/', methods=['GET'])
@login_required
def index():
  profile = read_token(request)
  prof_id = profile['id']
  journalEntries = Journal.query.filter_by(profile_id=prof_id).all()
  return jsonify([journal.serialize() for journal in journalEntries]), 200

@journalEntries.route('/<id>', methods=["PUT"])
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  journal = Journal.query.filter_by(id=id).first()

  if journal.profile_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(journal, key, data[key])

  db.session.commit()
  return jsonify(journal.serialize()), 200

@journalEntries.route('/<id>', methods=["DELETE"]) 
@login_required
def delete(id):
  profile = read_token(request)
  journal = Journal.query.filter_by(id=id).first()

  if journal.profile_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(journal)
  db.session.commit()
  return jsonify(message="Success"), 200