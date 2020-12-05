#import datetime
import datetime
import json

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import func

from lib.workshop import OnlineMod 

# Initialize Flask-SQLAlchemy
db = SQLAlchemy()


# JSon native support (text)
# =======================================

# See Json Support: https://www.michaelcho.me/article/json-field-type-in-sqlalchemy-flask-python


class GenericMixin(object):
    name = db.Column(db.String(255))

    created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow)


    @classmethod
    def paginate(cls, page=None, per_page=None):
        return cls.query.paginate(
            page=page,
            per_page=per_page, # or current_app.config['ITEMS_PER_PAGE'],
            error_out=True, 
            max_per_page=current_app.config['MAX_ITEMS_PER_PAGE']
            )


    # Other methods
    @classmethod
    def item_count(cls):
        '''Returns the number of mods'''
        return db.session.execute(db.session.query(cls).statement.with_only_columns([func.count()])).scalar()
        #return db.session.query(cls).count()
        #return db.session.execute(
        #            db.session
        #                .query(TableName)
        #                .filter_by(x_id=y.id)
        #                .statement.with_only_columns([func.count()]).order_by(None)
        #            ).scalar()



# User classes
# =======================================

# Define the User data-model.
# NB: Make sure to add flask_user UserMixin !!!
class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    serialize_only = ('id', 'first_name', 'last_name', 'email', 'email_confirmed_at', 'active')

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255, collation='NOCASE'), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')
    last_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

    playlists = db.relationship("Playlist", back_populates="user")


    def __repr__(self):
        return "<User(email='%s', first_name='%s', active='%s')>" % (
            self.email, self.first_name, self.active)


# Define the Role data-model
class Role(db.Model, SerializerMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model, SerializerMixin):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Mods classes
# =======================================

class Playlists2Mods(db.Model, SerializerMixin):
    '''Relationship table between playlists and mods'''
    __tablename__ = 'playlists_mods'
    serialize_only = ('mod_id', 'playlist_id', 'enabled', 'mod')

    mod_id = db.Column(db.Integer, db.ForeignKey('mods.id', ondelete="CASCADE"), primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id', ondelete="CASCADE"), primary_key=True)
    enabled = db.Column(db.String(50))

    mod = db.relationship("Mod", back_populates="playlists")
    playlist = db.relationship("Playlist", back_populates="mods")


class SteamAuthor(db.Model, SerializerMixin):
    '''Steam Workshop Authors'''
    __tablename__ = 'steamAuthors'

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow)
    author_profile_url = db.Column(db.String(255))
    author_image_url = db.Column(db.String(255))





class SteamMod(db.Model, SerializerMixin):
    '''Extra Steam Workshop Data''' 
    __tablename__ = 'steamMods'

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    #comments = db.Column(db.String(255))
    #mainpicture_url = db.Column(db.String(255))
    #changes_url = db.Column(db.String(255))
#
    #size = db.Column(db.String(255))
    #published = db.Column(db.DateTime())
    #updated = db.Column(db.DateTime())
#
    #changes_count = db.Column(db.Integer())
    #stars_count = db.Column(db.Integer())
    #visitor_count = db.Column(db.Integer())
    #subscribed_count = db.Column(db.Integer())
    #favored_count = db.Column(db.Integer())


    # Hashed
    mod_preview_url = db.Column(db.String(255))
    mod_desc = db.Column(db.Text())
    mod_type = db.Column(db.String(255))
    mod_requires = db.Column(db.Text())
    mod_tags = db.Column(db.Text())

    meta_size = db.Column(db.String(255))
    meta_published = db.Column(db.DateTime())
    meta_updated = db.Column(db.DateTime())
    meta_changes_url = db.Column(db.String(255))
    meta_changes_number = db.Column(db.Integer())

    meta_pic1_url = db.Column(db.String(255))


    # Unhashed
    com_stars = db.Column(db.Integer())
    com_ratings = db.Column(db.Integer())
    com_visitors = db.Column(db.Integer())
    com_subscribed = db.Column(db.Integer())
    com_fav = db.Column(db.Integer())

    com_comments = db.Column(db.Text())

    author_id = db.Column(db.Integer, db.ForeignKey('steamAuthors.id'), nullable=True)
    author = db.relationship(
        "SteamAuthor"
        )


class Mod(db.Model, GenericMixin, SerializerMixin):
    '''Game mod data'''
    __tablename__ = 'mods'
    serialize_only = ('id', 'steam_id', 'created', 'updated', 'name', 'steam_url', 
        'mod_preview_url',
        'mod_desc',
        'mod_requires',
        'mod_type',
        'mod_tags',
        'workshop_id',
        'workshop'
    )


    url_prefix='https://steamcommunity.com/sharedfiles/filedetails/?id='


    # Fields
    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(255))
    #created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    #updated = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow)

    steam_id = db.Column(db.String(255), nullable=False, unique=True, index=True)

    #mod_preview_url = db.Column(db.String(255))
    #mod_desc = db.Column(db.Text())
    #mod_requires = db.Column(db.String(255))
    #mod_type = db.Column(db.String(255))
    #mod_tags = db.Column(db.Text())


    # Relationships (Clone from workshop)
    mod_preview_url = db.Column(db.String(255))
    mod_desc = db.Column(db.Text())
    mod_type = db.Column(db.String(255))
    mod_requires = db.Column(db.Text())
    mod_tags = db.Column(db.Text())

    workshop_id = db.Column(db.Integer, db.ForeignKey('steamMods.id'), nullable=True)
    workshop = db.relationship(
        "SteamMod")
        #back_populates="id",
        #viewonly=True)

    playlists = db.relationship(
        "Playlists2Mods",
        back_populates="mod")

    # Other methods
    @staticmethod
    def mods_count():
        '''Returns the number of mods'''
        return db.session.execute(db.session.query(Mod).statement.with_only_columns([func.count()])).scalar()
        #return db.session.query(Mod).count()
        #return db.session.execute(
        #            db.session
        #                .query(TableName)
        #                .filter_by(x_id=y.id)
        #                .statement.with_only_columns([func.count()]).order_by(None)
        #            ).scalar()

    @property
    def steam_url(self):
        return f"{self.url_prefix}{self.steam_id}"

    # Fetch steam methods
    def fetchFromSteam(self):

        r = OnlineMod(self.steam_id)
        return r.parse()

    # Update steam methods
    def updateFromSteam(self):

        wmod = OnlineMod(self.steam_id)
        payload = wmod.parse()

        fields = [ i.name for i in self.__table__.columns ]

        mod = db.session.query(Mod).filter(Mod.id == self.id).one_or_none()
        if mod:

            print ('Saving mod ...')
            print (fields)
            for field in fields:
                if field in payload:
                    print (field)
                    value = payload[field]
                    setattr(mod, field, value)

            db.session.add(mod)
            db.session.commit()



        return payload

        ############ NEW

        pl = db.session.query(Playlist).filter(Playlist.name == pl_name, Playlist.id == pl_name).one_or_none()

        # Fetch or create playlist
        if pl:
            if user_id:
                pl.user_id=user_id

            if xml:
                print ("BUG ADD XML")
            
            db.session.add(pl)
            db.session.commit()

        else:
            pl = Playlist.createPlaylist(pl_name, user_id, xml=xml)

############ NEW


                

        #db.session.execute(
        #    db.session.query(Mod).statement.with_only_columns([func.count()])
        #    ).scalar()

        return payload


class Playlist(db.Model, GenericMixin, SerializerMixin):
    '''Playlist condifurations'''
    __tablename__ = 'playlists'
    serialize_only = ('id', 'name', 'created', 'updated', 'user_id', 'user', 'mods', 'file_hash', 'file_name', 'file_date')

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
    updated = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    description = db.Column(db.Text())
    #preview_url = db.Column(db.String(255))

    file_hash = db.Column(db.String(128))
    file_name = db.Column(db.String(128))
    file_date = db.Column(db.DateTime())

    # Relationships
    user = db.relationship("User", 
        back_populates="playlists")

    mods = db.relationship("Playlists2Mods",
        back_populates="playlist", cascade="all,delete")

    # Other methods
    def mods_count(self):
        '''Returns the number of mods'''
        print("Method mods_count", self)
        return db.session.query(Playlists2Mods.playlist_id).filter(Playlists2Mods.playlist_id==self.id).count()




    # OTHER METHODS (STATIC)
    
    def createPlaylist(name, user_id=None, xml=None, **kwargs):
        # Create the playlist
        pl = Playlist(
            name=name,
            **kwargs
        )
        
        db.session.add(pl)
        db.session.commit()

        return pl

    def updatePlaylist(pl_name, user_id=None, xml=None):
        pl = db.session.query(Playlist).filter(Playlist.name == pl_name, Playlist.id == pl_name).one_or_none()

        # Fetch or create playlist
        if pl:
            if user_id:
                pl.user_id=user_id

            if xml:
                print ("BUG ADD XML")
            
            db.session.add(pl)
            db.session.commit()

        else:
            pl = Playlist.createPlaylist(pl_name, user_id, xml=xml)
        
        return pl





def fillDB(db, app, user_manager):

    # Create 'member@example.com' user with no roles
    if not User.query.filter(User.email == 'member@example.com').first():
        user = User(
            email='member@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('qwerty'),
            first_name='Member',
        )
        db.session.add(user)
        db.session.commit()

    # Create 'admin@example.com' user with 'Admin' and 'Agent' roles
    if not User.query.filter(User.email == 'admin@example.com').first():
        user = User(
            email='admin@example.com',
            email_confirmed_at=datetime.datetime.utcnow(),
            password=user_manager.hash_password('qwerty'),
            first_name='Admin',
        )
        user.roles.append(Role(name='Admin'))
        user.roles.append(Role(name='Agent'))
        db.session.add(user)
        db.session.commit()


