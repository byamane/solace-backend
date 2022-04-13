from datetime import datetime
from api.models.db import db

class Journal(db.Model):
  __tablename__= 'journal_entries'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  date = db.Column(db.DateTime, default=datetime.utcnow)
  mood = db.Column(db.Integer, default=2)
  journal = db.Column(db.String())
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
  
  def serialize(self):
    journal = {s.name: getattr(self, s.name) for s in self.__table__.columns}
    return journal