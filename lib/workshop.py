import urllib
import re
from bs4 import BeautifulSoup  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from lib.tagging import TagManager, GenericItem

def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True

def conv_int(val):
    if is_int(val):
        return int(val)
    return 9999





class OnlineMod():

    url_prefix='https://steamcommunity.com/sharedfiles/filedetails/?id='

    def __init__(self, steam_id):
        self.steam_id=steam_id

        self.link = f"{self.url_prefix}{self.steam_id}"

        self.htmlpage=None
        self.steam_data=None

    def fetch(self):

        # Retrieving remote page
        if not self.htmlpage:
            print ("Fetching data: %s ..." % self.link)
            r = urllib.request.urlopen(self.link)
            print ("Done")
            html = r.read()
            self.htmlpage = html.decode("utf-8")
        else:
            print ("Using cached data for: %s" % self.link)


    def parse(self):

        if not self.htmlpage:
            self.fetch()

        # Soup the page
        soup = BeautifulSoup(self.htmlpage, "html.parser")
        details = {}

        # Workshop error handling
        message = soup.find(id="message")
        if message is not None:
            details["message"] = str(message.string)
            return details

        # Workshop item details
        content_ = soup.find(id="mainContents")
        if content_:

            # Extract header things (Name, rating and stars)
            title=None
            ratings=None
            stars=None
            mainpicture_url=None

            header_=content_.find(class_='workshopItemDetailsHeader')
            if header_:
                title = header_.find(class_='workshopItemTitle').text.strip()
                ratings_ = header_.find(class_='numRatings')
                if ratings_:
                    ratings_ = re.search('([0-9]+)', ratings_.text)
                    ratings = ratings_.group(1) if ratings_ else None

                stars_ = header_.find(class_='fileRatingDetails').img['src']
                stars_ = re.search('/([0-9])-star', stars_)
                stars = stars_.group(1) if stars_ else None

            # Extract Pictures Gallery Area ()
            mainpicture_url=None
            player_=content_.find(class_='highlight_overflow')
            if player_:

                mainpicture_url_=player_.find('img', id='previewImage')
                print(mainpicture_url_)

                if mainpicture_url_:
                    # Simple Image
                    mainpicture_url=re.sub('\?.*', '', mainpicture_url_['src'])
                else:
                    print ()
                    # Gallery system
                    #mainpicture_url=player_.find('div', id='highlight_strip')
                    #print(player_)
                    mainpicture_url_=player_.find("div", class_=["highlight_strip_item", "highlight_strip_screenshot"])

                    if mainpicture_url_:
                        mainpicture_url= re.sub('\?.*', '', mainpicture_url_.img['src'])

            # Extract Highlight Area (Thumbnail, tags and other infos)
            preview_url=None
            meta_size=None
            meta_published=None
            meta_updated=None
            tags=None
            changes_url=None
            changes_number=None
            type_=None

            highlight_ = content_.find(class_=['col_right', 'responsive_local_menu'])
            if highlight_:
                preview_url_ = highlight_.find("img", id='previewImageMain')
                if preview_url_:
                    preview_url=re.sub('\?.*', '', preview_url_['src'])

                meta_ = highlight_.find(class_='detailsStatsContainerRight').findAll(class_="detailsStatRight")
                if meta_:
                    for i in range(len(meta_)):
                        val=meta_[i].text
                        if i == 0:
                            meta_size = val
                        elif i == 1:
                            meta_published = val
                        elif i == 2:
                            meta_updated = val

                

                info_ = highlight_.find(class_='rightDetailsBlock')
                type_ = 'Asset'
                if info_:

                    tags_ = info_.find(class_='workshopTags', recursive=False)
                    if tags_:
                        tags=[ { 
                            'name': getattr(a, 'text', None),
                            'url': a.get('href', None)
                            } for a in tags_.findAll("a", href=True) ]

                    
                    type__ = info_.find("a", recursive=False)
                    type__ = getattr(type__, 'text', None)
                    if type__:
                        type_ = re.sub(':.*','', type__).strip()


                changes_ = highlight_.find(class_='detailsStatNumChangeNotes')
                if changes_:
                    changes_url = changes_.find('a')['href']
                    changes_number_ = changes_.text
                    changes_number_ = re.search('([0-9]+)', changes_number_)
                    changes_number = changes_number_.group(1) if changes_number_ else None


            # Extract Metadata Area (Right Column)
            metadata_ = content_.find(id='rightContents')
            author_profile_url=None
            author_image_url=None
            author_name=None
            stats_visitors=None
            stats_subscribed=None
            stats_fav=None
            requires=None
            comments=None
            details=None
            description=None

            if metadata_:
                requires_ = metadata_.find(id='RequiredItems')
                
                if requires_:
                    requires = []
                    for req in requires_.findAll("a"):
                        requires.append({
                            'name': req.text.strip(),
                            'url': req['href']
                        })

                author_ = metadata_.find(class_='friendBlock')
                if author_:
                    author_profile_url = author_.find("a", class_='friendBlockLinkOverlay')['href']
                    author_image_url = author_.find("img", )['src']
                    author_name_ = author_.find("div", class_='friendBlockContent')
                    author_name_.span.decompose()
                    author_name = author_name_.text.strip()

                stats_ = metadata_.find(class_='stats_table')
                if stats_:
                    counter = 0
                    for row in stats_.findAll('tr'):
                        val = re.sub('[^0-9]', '', str(row.findAll('td')[0].contents[0]))
                        if counter == 0:
                            stats_visitors = val
                        elif counter == 1:
                            stats_subscribed = val
                        elif counter == 2:
                            stats_fav = val
                        else:
                            break
                        counter = counter + 1
                    
            # Extract details
            details_ = content_.find(id='profileBlock')
            #title_ = details_.find(class_='game_area_purchase_game').h1.contents
            description = details_.find(id='highlightContent').prettify()

            comments_ = details_.find(class_='commentthread_comment_container')
            if comments_:
                comments = []
                for c in comments_.findAll(class_=['commentthread_comment', 'responsive_body_text']):

                    msg=c.find("div", class_='commentthread_comment_text').text.strip()
                    info=c.find("div", class_='commentthread_comment_author')
                    author=info.find("a", class_=['hoverunderline', 'commentthread_author_link']).text.strip()
                    date=info.find("span", class_='commentthread_comment_timestamp').text.strip()
                    creator=info.find("span", class_='commentthread_workshop_authorbadge')
                    if creator:
                        creator = True
                    else:
                        creator=False

                    comments.append({
                        "author": author,
                        "date": date,
                        "msg": msg,
                        "creator": creator
                    })




#    # Fields
#    id = db.Column(db.Integer, primary_key=True)
#    #name = db.Column(db.String(255))
#    #created = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow)
#    #updated = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow)
#
#    steam_id = db.Column(db.String(255), nullable=False, unique=True, index=True)
#    steam_url = db.Column(db.String(255))
#
#    mod_preview_url = db.Column(db.String(255))
#    mod_desc = db.Column(db.Text())
#    mod_requires = db.Column(db.String(255))
#    mod_type = db.Column(db.String(255))
#    mod_tags = db.Column(db.Text())

##    comments = db.Column(db.String(255))
##    mainpicture_url = db.Column(db.String(255))
##    changes_url = db.Column(db.String(255))
##
##    size = db.Column(db.String(255))
##    published = db.Column(db.DateTime())
##    updated = db.Column(db.DateTime())
##
##    changes_count = db.Column(db.Integer())
##    stars_count = db.Column(db.Integer())
##    visitor_count = db.Column(db.Integer())
##    subscribed_count = db.Column(db.Integer())
##    favored_count = db.Column(db.Integer())


            r = {
                'steam_id': self.steam_id,
                'steam_url': self.link,

                # Hashed
                'name': title,

                'mod_preview_url': preview_url,
                'mod_desc': description,
                'mod_type': type_,
                'mod_requires': requires,

                'meta_size': meta_size,
                'meta_published': meta_published,
                'meta_updated': meta_updated,
                'meta_changes_url': changes_url,
                'meta_changes_number': changes_number,

                'meta_tags': tags,
                'meta_pic1_url': mainpicture_url,

                # Unhashed
                'author_name': author_name,
                'author_profile_url': author_profile_url,
                'author_image_url': author_image_url,

                'com_stars': stars,
                'com_ratings': ratings,
                'com_visitors': stats_visitors,
                'com_subscribed': stats_subscribed,
                'com_fav': stats_fav,
                'com_comments': comments,

            }

            for k, v in r.items():
                if not type(v) in [str,list,dict,int] and v is not None:
                    print ("BUG: Steam fetch data key type error: %s (%s)" % (k, type(v)))
                    r[k] = str(v)

            self.steam_data=r
            return self.steam_data
    













#
#
#
#class MetaMod(GenericItem):
#
#    @db_session
#    def __init__(self, steam_id):
#        self.steam_id=str(steam_id)
#
#        self.meta=DBMod.get(workshop_id=self.steam_id)
#        self.local=None
#        self.online=None
#        self.workshop=WorkshopMod.get(ws_id=self.steam_id)
#
#
#        name=getattr(self.workshop, 'ws_title', 'Item %s' % steam_id )
#        self.initItem(id=steam_id, name=name )
#        
#    @db_session
#    def getSteam(self):
#        return self.workshop
#
#    def getLocal(self):
#        return self.local
#
#
#    def importsteam(self):
#        # Retrieve source data
#        omod=OnlineMod(self.steam_id)
#        
#        self.online=omod.fetch()
#
#
#    def displayforms(self):
#        
#        obj = WorkshopMod
#
#        print(WorkshopMod)
#        print(WorkshopMod.describe())
#
#        for i in range(len(WorkshopMod._converters_)):
#            #print (i)
#            name = WorkshopMod._columns_[i]
#            conv = WorkshopMod._converters_[i]
#            obj = WorkshopMod._attrs_[i]
#
#            print(obj.py_type)
#
#            print (i, obj.py_type, name, obj, conv.__class__.__name__, obj.desc)
#
#        #    print (i)
#        #    print (i.get_columns())
#        #    print(i.describe())
#        #    print (type(i))
#
#        toto = 67
#
#        return {}
#
#
#
#    def exportdb(self, update_steam=False):
#        
#        # Shortcuts
#        steam_id=self.steam_id
#        
#        # Update DB
#        with db_session:
#            # Retrieve parent mod
#            mod = DBMod.get(workshop_id=steam_id)
#            if not mod:
#                print ("Creating new meta mod: %s" % steam_id)
#                mod = DBMod(workshop_id=steam_id)
#            self.meta=mod
#            
#            # Refresh steam data if required
#            if update_steam and self.online is None:
#                self.importsteam()
#
#            # Add to DB the record if any data
#            if self.online:
#                db_data=self.online
#                wsmod=WorkshopMod.get(ws_id=steam_id)
#
#                # Create entity if not present
#                if not wsmod:
#                    print ("Creating new workshop mod: %s" % steam_id)
#                    wsmod = WorkshopMod(db_mod=mod)
#                else:
#                    wsmod.db_mod=mod
#
#                for k, v in db_data.items():
#                    if v:
#                        setattr(wsmod, k, v)
#
#                # Update links
#                mod.workshop_mod=wsmod
#                mod.workshop_id=steam_id
#
#            commit()
#
#        return True
#
#    @staticmethod
#    def list_mods():
#        '''Retrieve all metamods'''
#        items=[]
#        with db_session():
#            for p in select(p for p in DBMod):
#                #print (p.steam_id)
#                #print (p.steam_id)
#                items.append(MetaMod(p.workshop_id))
#        return items
#
#
#    @classmethod
#    def displaytree(cls):
#
#        modlist = cls.list_mods()
#
#        print (modlist)
#        modtree={}
#        for i in modlist:
#            print (type(i))
#            ws = i.workshop
#            print (dir(ws))
#            if not ws:
#                continue
#            cat = ws.ws_type or 'None'
#            tags = ws.com_tags or [{'name': 'Unknown'}]
#
#            #print("stop")
#
#            # Create cat dict
#            if not cat in modtree:
#                modtree[cat]={}
#
#            for t in tags:
#
#                # Retrieve tags
#                tag_name=t['name'] or 'Empty Tag'
#
#                # Create tag dict
#                if not tag_name in modtree[cat]:
#                    modtree[cat][tag_name]=[]
#
#                modtree[cat][tag_name].append(i)
#
#        #print (modtree)
#
#
#        modorder=[]
#        for cat in ['Mod', 'SaveGame', 'Map', 'Map Theme'] + [k for k in modtree.keys()]:
#            if cat in modtree:
#            
#                tags = list(modtree[cat].keys()) or ['None']
#                print (tags)
#                if cat == 'Mod':
#                    tags.sort(key=lambda s: [ conv_int(u) for u in s.split('.')])
#
#                else:
#                    tags.sort()
#                print (tags)
#
#                e = {
#                    'cat': cat,
#                    'tags': tags
#                }
#                if e not in modorder: 
#                    modorder.append(e)
#                    
#        print (modorder)
#
#        return (modlist,modtree,modorder)
#
#
#
#
#
#
#
#
#
#
#
#
