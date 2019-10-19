import os
import sys
import flask
from feapp.infrastructure.view_modifiers import response
import feapp.data.db_session as db_session
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)

app = flask.Flask(__name__)


def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'glaceon.sqlite')

    db_session.global_init(db_file)


def main():
    register_blueprints()
    setup_db()
    app.run(debug=True, port=5006)

def configure():
    register_blueprints()
    setup_db()

def register_blueprints():
    from feapp.views import home_views
    from feapp.views import stream_views
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(stream_views.blueprint)


if __name__ == '__main__':
    main()
else:
    configure()
