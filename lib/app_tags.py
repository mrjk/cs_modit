
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify, Blueprint
from flask_paginate import Pagination, get_page_args, get_parameter

from lib.workshop import *

app = Blueprint('tags', __name__, template_folder='templates')



@app.route('/tags/list')
def pl_tags():
    '''List all tags'''

    from lib.tagging import TagManager
    import random


    T=TagManager()


    # Tags:
    ttype = T.addTagType("ModType")
    ttags = T.addTagType("ModTags")

    # Assets
    #tasset = T.addTagType("Assets")
    #for tag in ['Building', 'Health', 'Electricity', 'Education']:
    #    tasset.addTag(tag)
#
    ## Playlists
    #tplaylist = T.addTagType("PlayList")
    #tplaylist.addTag('jez2')
    #tplaylist.addTag('jez22')
    #tplaylist.addTag('Yoliiist')
    #tplaylist.addTag('SuperList')
    #tplaylist.addTag('jezdsfdsf')
    #
    #tag_jezselec = tplaylist.addTag('jez1')
#
    # Apply on mods
    mods = MetaMod.list_mods()
    select = random.choices(mods, k=40)
    select=mods
    for mod in select:
        print ("Linking: %s" % mod)
        print (mod.workshop.ws_type)

        genre=mod.workshop.ws_type or '0 NoType'
        ttype.link(obj=mod, tag_name=genre)

        tags=mod.workshop.com_tags
        if len(tags) < 1:
            if mod.workshop.ws_type != 'Asset':
                tags=[{'name': '0 %ss' % mod.workshop.ws_type }]
            else:
                tags=[{'name': '0 Untagged Assets'}]

        for tag in tags:
            tag_name=tag.get('name').strip()
            ttags.link(obj=mod, tag_name=tag_name)



    data=T.jsonTree(tagtypes="ModTags")

    return render_template('tags_main.html', data=data, jsdata=data)



