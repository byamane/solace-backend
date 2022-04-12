from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from api.models.db import db
from config import Config

# ============ Import Models ============
from api.models.user import User
from api.models.profile import Profile
from api.models.sleep import Sleep
from api.models.journal import Journal

# ============ Import Views ============
from api.views.auth import auth
from api.views.sleepLogs import sleepLogs
from api.views.journalEntries import journalEntries

cors = CORS()
migrate = Migrate() 
list = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'LINK']

def create_app(config):
  app = Flask(__name__)
  app.config.from_object(config)

  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app, supports_credentials=True, methods=list)

  # ============ Register Blueprints ============
  app.register_blueprint(auth, url_prefix='/api/auth') 
  app.register_blueprint(sleepLogs, url_prefix='/api/sleep')
  app.register_blueprint(journalEntries, url_prefix='/api/journal')


  return app

app = create_app(Config)