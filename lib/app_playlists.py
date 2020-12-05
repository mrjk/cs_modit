
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, Blueprint, jsonify, make_response
from flask_user import current_user, login_required, roles_required
from flask_restful import Api, reqparse, abort, Resource
from flask_paginate import Pagination, get_page_args, get_parameter

#from lib.workshop import *
#from lib.database import *
from lib.database import db, Playlist
import datetime


app = Blueprint('app_playlist', __name__, template_folder='templates')


# https://github.com/jazzband/django-taggit
# https://tmsu.org/
# https://github.com/sirkubax/pyTagVFS



# Rest API
# ==========================================

class restPlaylist(Resource):
    '''Manage playlist'''

    def get(self, playlist_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rate', type=int, help='Rate to charge for this resource')
        args = parser.parse_args()

        pl = Playlist.query.get(playlist_id)
        data = pl.to_dict()
        return make_response(jsonify(data), 200)

    @login_required
    def delete(self, playlist_id):
        pl = Playlist.query.get(playlist_id)
        db.session.delete(pl)
        db.session.commit()
        data = { 'status': 'deleted'}
        return make_response(jsonify(data), 200)

    @login_required
    def put(self, playlist_id):
        args = parser.parse_args()
        playlist_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        playlist_id = 'todo%i' % playlist_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[playlist_id], 201


class restPlaylists(Resource):
    '''Manage playlists'''

    def get(self):
        d = db.session.query(Playlist).all()
        d= [ pl.to_dict(rules=('id', '-mods', 'item_count')) for pl in d]
        return d

    def post(self):
        return None


api = Api(app) 
api.add_resource(restPlaylists, '/api/playlist/', endpoint='rest_playlists')
api.add_resource(restPlaylist, '/api/playlist/<playlist_id>', endpoint='rest_playlist')


# Web interface
# ==========================================



@app.route('/playlists/')
def pl_list():
    '''List all playlists'''
    pl_list=[]
    for pl in db.session.query(Playlist).all():
        pl_list.append(pl)
    return render_template('playlists/list.html', data_list=pl_list)


@app.route('/playlist/<int:playlist_id>')
def pl_show_id(playlist_id):
    pl = Playlist.query.get(playlist_id)
    return render_template('playlists/show.html', item=pl)




    
@app.route('/playlist/create', methods=('GET', 'POST'))
@login_required
def pl_create():
    '''Create new mod reference'''
    if request.method == 'POST':
        pl_name = request.form['pl_name']

        #pl = createPlaylist(db, pl_name, current_user.id)
        pl = Playlist.createPlaylist(pl_name, user_id=current_user.id)

        #file = request.files['file']
        ## if user does not select file, browser also
        ## submit an empty part without filename
        #if file.filename == '':
        #    flash('No selected file')
        #    return redirect(request.url)
        #if file and allowed_file(file.filename):
        #    filename = secure_filename(file.filename)
        #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Fetch file config
        f = '/home/jez/.local/share/Colossal Order/Cities_Skylines/Addons/Mods/ModsList/ModsList_savefiles/NewBase2020 v5 - beta.xml'
        xml, hash = readModListFile(f)
        mod_list, asset_list=modlist2dict(xml)
        AddFromXML(db, pl, mod_list)        

        url=url_for('playlist.pl_show_id', playlist_id=pl.id )
        return redirect(url)

    elif request.method == 'GET':
        return render_template('playlists/create.html', data={})




@app.route('/playlist/json/<int:playlist_id>')
def pl_json_id(playlist_id):
    pl = Playlist.query.get(playlist_id)
    data = pl.to_dict()
    return make_response(jsonify(data), 200)


@app.route('/playlist/delete/<int:playlist_id>')
def pl_delete_id(playlist_id):
    pl = Playlist.query.get(playlist_id)
    db.session.delete(pl)
    db.session.commit()
    return redirect(url_for('playlist.pl_list'))


#@login_required
@app.route('/playlist/import')
def pl_import():
    user_id=getattr(current_user, 'id', None)
    importLocal(db, user_id)
    return redirect(url_for('playlist.pl_list'))




# Library

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'xml'}


def modlist2dict(dataxml):
    import xml.etree.ElementTree as ET
    xmlroot = ET.fromstring(dataxml)

    mod_list=[]
    for i in xmlroot.findall('./Mods/ModEntry'):
        attr=i.attrib
        r = {
            'name': attr.get( 'name', 'Missing'),
            'id': attr.get( 'ID', None),
            'activated': attr.get( 'activated', None),
        }
        mod_list.append(r)

    asset_list=[]
    for i in xmlroot.findall('./Assets/AssetEntry'):
        attr=i.attrib
        r = {
            'name': attr.get( 'name', 'Missing'),
            'id': attr.get( 'ID', None),
            'activated': attr.get( 'activated', None),
        }
        asset_list.append(r)

    district_list=[]
    for i in xmlroot.findall('./DistrictStyle/DistrictStyleEntry'):
        attr=i.attrib
        r = {
            'name': attr.get( 'name', 'Missing'),
            'id': attr.get( 'ID', None),
            'activated': attr.get( 'activated', None),
        }
        district_list.append(r)

    return (mod_list, asset_list)




def readModListFile(f):

    with open(f, 'r', encoding='utf-16') as file:
        dataxml = file.read()

    import hashlib

    hash_md5 = hashlib.md5()
    with open(f, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    hash=hash_md5.hexdigest()



    return dataxml, hash


def AddFromXML(db, pl, mod_list, mod_type):
    # Fetch the mods
    for mod_dict in mod_list:
        name=mod_dict.get('name', 'UnNamed')
        steam_id=mod_dict.get('id', "0")
        activated=mod_dict.get('activated', 'None')

        mod = db.session.query(Mod).filter(Mod.steam_id == steam_id).one_or_none()
        if not mod:
            mod = Mod(
                steam_id=steam_id,
                name=name,
                created=datetime.datetime.utcnow(),
                updated=datetime.datetime.utcnow(),
                mod_type=mod_type
            )
            db.session.add(mod)

        a = db.session.query(Playlists2Mods).filter(Playlists2Mods.playlist == pl, Playlists2Mods.mod == mod).one_or_none()
        if not a:
            assoc = Playlists2Mods(enabled = activated, 
                mod=mod,
                playlist=pl,
                )
            db.session.add(assoc)            
            
    db.session.add(pl)
    db.session.commit()


def importLocal(db, user_id):

    folder = '/home/jez/.local/share/Colossal Order/Cities_Skylines/Addons/Mods/ModsList/ModsList_savefiles/'

    import os


    for root, dirs, files in os.walk(folder):
        for file_name in files:
            if file_name.endswith(".xml"):
                pl_name = os.path.splitext(file_name)[0]
                f=os.path.join(root, file_name)

                print ("importing file: ", f, file_name)

                xml, file_hash = readModListFile(f)
                
                mod_list, asset_list=modlist2dict(xml)
                print ("HASH", hash, mod_list)

                #pl = db.session.query(Playlist).filter(Playlist.file_hash == file_hash).one_or_none()
                pl = db.session.query(Playlist).filter(Playlist.file_hash == file_hash, Playlist.file_name == file_name).one_or_none()
                if not pl:
                    #pl = Playlist.createPlaylist(pl_name, user_id=user_id, file_hash=file_hash)
                    pl = Playlist.createPlaylist(pl_name, user_id=user_id, file_name=file_name, file_hash=file_hash)

                AddFromXML(db, pl, mod_list, 'Mod')
                AddFromXML(db, pl, asset_list, 'Asset')

                print ("Mod IMPORTEDDDD")









# DEPRECATED FUNCTIONS


def createPlaylist(db, pl_name, user_id):
    print ("createPlaylist IS DEPRECATED")
    # Create the playlist
    pl = Playlist(
        name=pl_name,
        created=datetime.datetime.utcnow(),
        updated=datetime.datetime.utcnow(),
        user_id=user_id,
    )
    
    db.session.add(pl)
    db.session.commit()
    return pl