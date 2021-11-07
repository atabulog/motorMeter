"""
Initalizer file for application instances
"""
# imports
from os import path, makedirs
from flask import Flask, render_template

# application factory function
def create_app(test_config=None):
    """Creates app instance and sets config settings.
    Args:
        test_config (path): location of configuration file for application.
    Returns:
        None.
    """
    # create and configure flask to be instance relative
    app = Flask(__name__, instance_relative_config=True)
    # set database mapping to app path relative location
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=path.join(
        app.instance_path, "testApp.sqlite"))

    # set config file location if not given
    if test_config is None:
        # load instance config if exists when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load config if passed in
        app.config.from_mapping(test_config)

    # create application instance folder if one DNE.
    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    # ceate base landing page.
    @app.route("/")
    def home():
        return render_template("base.html")

    #define connection to sqlite database
    from . import db
    db.init_app(app)

    #add interaction blueprint to flask app
    from . import interaction
    app.register_blueprint(interaction.bp)

    #add settings blueprint to flask app
    from . import settings
    app.register_blueprint(settings.bp)

    #return application to flask
    return app

if __name__ == '__main__':
    app=create_app()
    app.run(host="0.0.0.0", port=80)
