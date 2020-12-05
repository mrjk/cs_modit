
import datetime
from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_user import UserManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from lib.env import DATA_DIR
from lib.database import db, User, Role, Mod, Playlist, fillDB


#from lib.app_admin import app as app_admin
from lib.app_workshop import app as app_workshop
from lib.app_playlists import app as app_playlists
from lib.app_tags import app as app_tags
from lib.app_users import app as app_users

#from lib.rest.playlists import restPlaylist, restPlaylists

DB_FILE = str( DATA_DIR / 'database.sqlite' )

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    UPLOAD_FOLDER = 'uploads/'
    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILE    # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Avoids SQLAlchemy warning
    print ("DATABASE FILE", SQLALCHEMY_DATABASE_URI)

    # Flask-Mail SMTP server settings
    #MAIL_SERVER = 'smtp.gmail.com'
    #MAIL_PORT = 465
    #MAIL_USE_SSL = True
    #MAIL_USE_TLS = False
    #MAIL_USERNAME = 'email@example.com'
    #MAIL_PASSWORD = 'password'
    #MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

    # Flask-User settings
    USER_APP_NAME = "Cities Skylines: Play It!"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = False        # Enable email authentication
    USER_ENABLE_USERNAME = False    # Disable username authentication
    #USER_EMAIL_SENDER_NAME = USER_APP_NAME
    #USER_EMAIL_SENDER_EMAIL = "noreply@example.com"

    BUNDLE_ERRORS=True


def create_app():
    """ Flask application factory """
    
    # Create Flask app load app.config
    app = Flask(__name__)
    app.config.from_object(__name__+'.ConfigClass')


    app.config['SQLALCHEMY_ECHO'] = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['MAX_ITEMS_PER_PAGE'] = None
    app.config['ITEMS_PER_PAGE'] = 25

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    
    app.debug = True
    toolbar = DebugToolbarExtension(app)



    admin = Admin(app, name='CS: Play It! Settings', template_mode='bootstrap4')
    admin.add_view(ModelView(Mod, db.session))
    admin.add_view(ModelView(Playlist, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))



    # Init DB
    db.init_app(app)
    with app.app_context():
        db.create_all()
        # Setup Flask-User and specify the User data-model
        user_manager = UserManager(app, db, User)
        fillDB(db, app, user_manager)


    # Import middleware
    app.register_blueprint(app_workshop)
    app.register_blueprint(app_playlists)
    app.register_blueprint(app_tags)
    app.register_blueprint(app_users)

    # Configure default page
    @app.route('/')
    def index():
        '''Welcome page'''
        return redirect(url_for('workshop.mod_list'), code=302)

    return app


# Start development web server
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)


