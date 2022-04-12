from datetime import datetime
from api.models.db import db

class Sleep(db.Model):
  __tablename__= 'sleep_logs'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  rating = db.Column(db.Integer, default=1)
  notes = db.Column(db.String(500))
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
  
  def serialize(self):
    sleep = {s.name: getattr(self, s.name) for s in self.__table__.columns}
    return sleep