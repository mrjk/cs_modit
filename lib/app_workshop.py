
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, Blueprint, current_app, make_response
from flask_user import current_user, login_required, roles_required
from flask_restful import Api, reqparse, abort, Resource
from flask_sqlalchemy import SQLAlchemy

from webargs import fields, validate
from webargs.flaskparser import parser, use_args

#from lib.workshop import OnlineMod
from lib.database import db, Mod
from lib.common import Paginate





app = Blueprint('workshop', __name__, template_folder='templates')

#max_items_pp=current_app.config['MAX_ITEMS_PER_PAGE']




user_args = {
    # Required arguments
    "username": fields.Str(required=True),
    # Validation
    "password": fields.Str(validate=lambda p: len(p) >= 6),
    # OR use marshmallow's built-in validators
    "password": fields.Str(validate=validate.Length(min=6)),
    # Default value when argument is missing
    "display_per_page": fields.Int(missing=10),
    # Repeated parameter, e.g. "/?nickname=Fred&nickname=Freddie"
    "nickname": fields.List(fields.Str()),
    # Delimited list, e.g. "/?languages=python,javascript"
    "languages": fields.DelimitedList(fields.Str()),
    # When value is keyed on a variable-unsafe name
    # or you want to rename a key
    "user_type": fields.Str(data_key="user-type"),
}
args_pagination = {
    "p": fields.Int(missing=1),
    "pp": fields.Int(missing=25),
}
args_mod = {
    "source": fields.Str(
        missing="none",
        
        )
}




# Rest API
# ==========================================

class restMod(Resource):

    #@use_args(args_mod)
    def get(self, steam_id):

        #args = parser.parse(args_mod, request)
        #print ("ARGS", args)

        mod=Mod.query.filter(Mod.steam_id == str(steam_id)).one_or_none()
        return make_response(mod.to_dict(), 200)


class restMods(Resource):

    def get(self):

        args = parser.parse(args_pagination, request)
        mods = Mod.paginate(args['p'], args['pp']).items
        return [ mod.to_dict() for mod in mods ]


api = Api(app)
api.add_resource(restMods, '/api/mods/', endpoint='rest_mods')
api.add_resource(restMod, '/api/mod/<steam_id>', endpoint='rest_mod')



# Web interface
# ==========================================


@app.route('/mods/')
@use_args(args_pagination, location="query")
def mod_list(args):
    '''Show the list of mods'''
    print("ARGS", args)
    p = Paginate(Mod, page=args['p'], per_page=args['pp'])
    return render_template('mods/list.html', items=p.items, pagination=p)


@app.route('/mod/<int:steam_id>')
def mod_show_id(steam_id):
    '''Show a mod'''

    mod = db.session.query(Mod).filter(Mod.steam_id == str(steam_id)).one_or_none()
    if mod:
        return render_template('mods/show.html',
        item=mod.to_dict())
    else:
        return make_response(render_template("layout/http_4xx.html"), 404)



@app.route('/mod/steam/<int:steam_id>')
def mod_fetch_steam_id(steam_id):
    mod=Mod.query.filter(Mod.steam_id == str(steam_id)).one_or_none()
    r = mod.updateFromSteam() or {"ERROR":"EROOOOOOOOOORRR"}

    print ("YOOO", r)

    print (mod.steam_data)

    return make_response(r, 200)






########## DEPRECATED






#@app.route('/workshop/show/<int:steam_id>')
#def ws_mod_show(steam_id):
#    '''Show a mod'''
#    meta_mod=MetaMod(steam_id)
#
#    meta_mod.displayforms()
#
#    return render_template('ws_mod_show.html', 
#        id=steam_id,
#        meta_mod=meta_mod, 
#        steam_mod=meta_mod.getSteam(),
#        local_mod=meta_mod.getLocal())




#@app.route('/workshop/list')
#def ws_mod_index():
#    '''List all mods'''
#    items = MetaMod.list_mods()
#
#
#    page, per_page, offset = get_page_args(
#        page_parameter="p", 
#        per_page_parameter="pp",
#        pp=25,
#    )
#
#    search = False
#    q = request.args.get('q')
#    if q:
#        search = True
#    
#    pagination = get_pagination(
#        p=page,
#        pp=per_page,
#        total=len(items),
#        record_name="item",
#        format_total=False,
#        format_number=True,
#        page_parameter="p",
#        per_page_parameter="pp",
#        search=search,
#        generate_pp=generate_pp,
#    )
#
#    items = items[offset:offset+per_page]
#
#    return render_template('ws_mod_index.html', items=items, pagination=pagination)
#

# @app.route('/workshop/tree')
# def ws_mod_tree():
#     '''List all mods with a treview'''
# 
#     modlist,modtree,modorder = MetaMod.displaytree()
#     return render_template('ws_mod_tree.html', tree=modtree, order_list=modorder)

@app.route('/workshop/create', methods=('GET', 'POST'))
def ws_mod_create():
    '''Create new mod reference'''
    if request.method == 'POST':
        steam_id = request.form['steam_id']
        url=url_for('workshop.ws_mod_create_id', steam_id=steam_id )
        return redirect(url)
    elif request.method == 'GET':
        return render_template('ws_mod_create.html')

@app.route('/workshop/create/<int:steam_id>')
def ws_mod_create_id(steam_id):
        meta_mod=MetaMod(steam_id)
        meta_mod.importsteam()
        meta_mod.exportdb()
        return redirect(url_for('workshop.ws_mod_show', steam_id=int(steam_id)))



@app.route('/workshop/edit/<int:steam_id>')
def ws_mod_edit(steam_id):
    mod = MetaMod(steam_id)    
    return render_template('ws_mod_edit.html', id=id, mod=mod)

@app.route('/workshop/json/<int:steam_id>')
def ws_mod_update_steam(steam_id):
    meta_mod=MetaMod(steam_id)
    meta_mod.importsteam()
    return jsonify(meta_mod.online)






