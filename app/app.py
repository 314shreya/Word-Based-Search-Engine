from flask import Flask
from flask_cors import CORS

from werkzeug.middleware.proxy_fix import ProxyFix
from app.initializers.InitializeApp import InitializeApp
from app.initializers.register_all_blueprints import RegisterBlueprints
import os
# from initializers.register_all_blueprints import RegisterBlueprints

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_port=1)

# with app.app_context():
# from services.setup_config import SetupConfig
# SetupConfig(app)
# db.init_app(app)

# RegisterBlueprints(app, db)
CORS(app)
RegisterBlueprints(app)
InitializeApp()
app.config['JWT_TOKEN_LOCATION'] = ['headers']
# port = int(os.environ.get("PORT", 5002))
# app.run(threaded=True, port=port, debug=True)

# print("...Default Web Mode Completed")
