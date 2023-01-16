from app.api.search_api import search_blueprint


class RegisterBlueprints:

    def __init__(self, app):
        app.register_blueprint(search_blueprint)
