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
def index():
  journalEntries = Journal.query.all()
  return jsonify([journal.serialize() for journal in journalEntries]), 200