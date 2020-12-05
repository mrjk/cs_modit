



####################################### The store !


class Store():
    '''An Store controller object to save and access data into other objects.'''

    def __init__(self, name='default', fnValidate=None):
        self.store={}
        self.name=name

    @staticmethod
    def fnValidate(value):
        return True

    def addKey(self, key, value=None):

        if valueFn:
            fnValidate=fnValidate

        self.store[key]={'name': key}
        self.setKeyValue(key, value)
        return value

    def rmKey(self, key):
        if not key in self.store:
            return False
        self.store.pop(key)
        return True

    def getKey(self, key):
        if key in self.store:
            return self.store[key]
        return None

    def getKeys(self):
        return self.store.keys()

    def setKeyValue(self, key, value):
        if not self.fnValidate():
            raise Exception('Value type {} is not allowed for {} store (key={})'.format(value, key, self.name))
        self.store[key]['value']=value
        return True

    def getTagValue(self, key):
        if not key in self.store:
            raise Exception('Key {} does not exists in {} store'.format(key, self.name))
        return self.store[key]['value']

    def dump(self):
        return self.store

    def debug(self):
        print('Dump content of Store {} ({} keys)'.format(self.name, len(self.store)))
        for k,v in self.store.items():
            print ('Key: {}={}'.format(k, v['value']))
        return self.store







#################################### Public API

import uuid
import json

class TagManager(Store):
    '''This is the tag manager'''

    def __init__(self):
        #self.tagtype_store = Store(name='TagsTypes')
        self.tagtype_store={}
        pass


    # API methods of Tags
    def addTagType(self, name, config=None, tags=None):
        tagtype= TagType(self, name, config=config, tags=tags)
        self.tagtype_store[name] = tagtype
        return tagtype

    def rmTagType(self, name):
        self.tagtype_store.remove(name)
        return None

    def getTagTypes(self):
        return self.tagtype_store

    def getTagType(self, name):
        #tagtype = self.tagtype_store.get(name, None)
        if name in self.tagtype_store:
            return self.tagtype_store[name]
        return tagtype

    #def setTagType(self, name, config=None):
    #    tagtype = getTagType(name)
    #    tagtype = self.tagtype_store.get(name, None)
    #    return tagtype



    # Dump stuffs
    def dumpTree(self):
        tagtypes = self.getTagTypes()

        print ("Number of TagTypes: {}".format(len(tagtypes)))
        for tagtype_name, tagtype in tagtypes.items():
            
            print('* TagType name: %s (%s)' % (tagtype.name, tagtype))
            
            # Check Tags
            tags=tagtype.getTags()
            print ('  - Number of tags: %s' % len(tags))
            for tag_id, tag in sorted(tags.items(), key=lambda x: x.name):
                print ("    - %s (%s)" % (tag.name, tag.id))
                for o in tag.getObjs():
                    print ("      - %s" % o.name)

            # Check Objs
            objs=tagtype.getObjs()
            print ('  - Number of objs: %s' % len(objs))
            for obj_id, obj in objs.items():
                print ("    - %s: %s" % (obj.id, obj.name))
                for t in obj.getTags():
                    print ("      - %s" % t.name)

    def jsonTree(self, tagtypes=None):

        if not tagtypes:
            _tagtypes = self.getTagTypes()

        if isinstance(tagtypes, str):
            _tagtypes = {tagtypes: self.getTagType(tagtypes)}
        if isinstance(tagtypes, list):
            _tagtypes=[self.getTagType(t) for t in tagtypes]
            _tagtypes={ t.name: t for t in _tagtypes}
        
        if not _tagtypes:
            raise Exception('Tag type %s is not found' % _tagtypes)
        tagtypes=_tagtypes

        print ('tagtypes', tagtypes)

        n0=[]

        for tagtype_name, tagtype in tagtypes.items():
            print (tagtype)

            n1_text='%s' % tagtype.name
            n1_nodes=[]
            
            tags=tagtype.getTags()
            for tag_id, tag in sorted(tags.items(), key=lambda v: v[1].name):
                n2_text="%s" % tag.name # (%s)" % (tag.name, tag.id)
                n2_nodes=[{'text': str(o.name), 'steam_id': str(o.id)} for o in sorted(tag.getObjs(), key=lambda v: v.name)]

                if len(n2_nodes) > 0:
                    n1_nodes.append({
                        'text': n2_text,
                        'nodes': n2_nodes,
                        'tags': [len(n2_nodes)],
                        'selectable': False,
                    })

            n0.append({
                'text': n1_text,
                'nodes': n1_nodes,
                'tags': [len(tags)],
                'selectable': False,
            })

        #print (n0)
        return json.dumps(n0)





#################################### Object classes


class GenericItem():

    #id=None
    #name=None
    #data=None

    def initItem(self, id=None, name=None, data=None):
        self.id=str(id or uuid.uuid4())
        self.name=str(name or "Item: {}".format(id))
        self.data=data


class TagItem(GenericItem):
    '''Contained into the manager structure'''

    def __init__(self, tag_type, name, id=None):
        self.initItem(id=id, name=name)
        self.tag_type = tag_type
        self.tag_store = self.tag_type.tag_store
        self.obj_list=[]

    # API methods for Objs
    def addObj(self, obj):
        if not obj in self.obj_list:
            self.obj_list.append(obj)
        return obj

    def rmObj(self, obj):
        if obj in self.obj_list:
            self.obj_list.pop(obj)
        return obj

    def getObj(self, obj):
        if obj in self.obj_store:
            return obj
        return None

    def getObjs(self):
        '''Returns a list of Objs'''
        return self.obj_list



class ObjItem(GenericItem,Store):
    '''Contained into the object structure'''

    

        # ObjItem: __init__(self, tag_type, obj, id, name=None):

    def __init__(self, tag_type, obj, id=id, name=None):
        self.initItem(id=id, name=name)
        self.tag_type = tag_type
        self.obj_store = self.tag_type.obj_store
        self.tag_store = self.tag_type.tag_store
        self.tag_list=[]

        self.obj=obj


    # API methods for Tags
    def addTag(self, tag):
        if not tag in self.tag_list:
            self.tag_list.append(tag)
        return tag

    def rmTag(self, tag):
        return self.tag_list.pop(tag)

    def getTag(self, tag):
        if tag in self.tag_store:
            return tag
        return None

    def getTags(self):
        '''Returns a list of Tags'''
        return self.tag_list


# TagType class
class TagType(GenericItem):
    '''This is a tagtype'''



    def tagValueCheck(self, value):
        if value is None or \
            type(value) == int or \
            type(value) == str or \
            type(value) == bool:
            return True
        raise Exception('Invalid value {} type for tag, must be: str, int or bool'.format(str(value)))
        return False
            
    def tagNameCheck(self, value):
        return True


    name=None
    tagmanager_ref=None
    #tag_store={}
    #obj_store={}
    config={
        'tagNameCheck': tagNameCheck,
        'tagValueCheck': tagValueCheck
    }



    def __init__(self, tagmanager, name, config=None, tags=None):
        self.initItem(id=id, name=name)
        self.tagmanager_ref=tagmanager
        self.name=name

        if config:
            self.config=config
        self.tag_store=tags or {}
        self.obj_store={}


    def findItem(self, item, key):
        assert (item in ['obj', 'tag'])

        if item == 'obj':
            store=self.tag_store
        else:
            store=self.obj_store

        # Fast access
        if key in store:
            return store[key]

        # Name and value lookup
        t = [v for k, v in self.tag_store.items() if (v.name == key or v == key)]
        return next(iter(t), None)


    # API methods for Objs, fill TagManager objects db
    def addObj(self, obj):
        obj = ObjItem(self, obj, id=obj.id, name=obj.name)
        # ObjItem: __init__(self, tag_type, obj, id, name=None):
        self.obj_store[obj.id] = obj
        return obj

    def rmObj(self, obj_id):
        self.obj_store.remove(obj_id)
        return None

    def getObjs(self):
        return self.obj_store

    def getObj(self, obj_id, create=False):
        obj = self.findItem('obj', obj_id)
        if not obj and create == True:
            obj = self.addObj(obj, obj_id=obj_id)
        return obj

    # API methods for Tags
    def addTag(self, tag, tag_name=None):
        tag_name=str( tag_name or tag)
        tag = TagItem(self, id=None, name=tag_name )
        # TagItem: def __init__(self, tag_type, name, value=None, id=None):
        self.tag_store[tag.id]=tag
        return tag

    def rmTag(self, tag):
        tag = self.findItem('tag', tag)
        return self.tag_store.pop(tag.id)

    def getTag(self, tag, create=False, tag_name=None):
        tag = self.findItem('tag', tag)
        if not tag and create == True:
            tag = self.addTag(tag, tag_name=tag_name)
        return tag

    def getTags(self):
        return self.tag_store


    # Linking methods
    def link(self, obj=None, tag=None, tag_name=None):

        obj_ = self.getObj(obj)
        if not obj_:
            obj_ = self.addObj(obj)
        obj=obj_

        tag = self.getTag(tag or tag_name, create=True, tag_name=tag_name)

        obj.addTag(tag)
        tag.addObj(obj)

    def unlink(self, obj, tag):
        obj = self.getObj(obj)
        tag = self.getTag(tag)

        obj.rmTag(tag)
        tag.rmObj(obj)


#################################### DEPRECATED




class TaggableItem(GenericItem):
    '''Contained into the manager structure'''

    def __init__(self, tag_type, name, id=None):
        self.initItem(id=id, name=name)
        self.tag_type = tag_type
        self.tag_store = self.tag_type.tag_store
        self.obj_list=[]




#     
#     
#     class Tagged():
#         '''Class that must be to be inherited on objects that need to be tagged'''
#     
#         _tag_store={}
#         _tag_default_store='tag'
#         _tag_mgr=None
#     
#     
#         _tag_id=None
#         _tag_default_type=None
#         _tag_data={}
#     
#     #        tagtype.name: 
#     #            tagtype_ref: 
#     #            tag_data: Store()
#     #                key: {key, value, other ....}
#     #
#     #    }
#     
#         # Init functions
#         def initTags(self, tagtype, obj_id=None, default=False):
#     
#             # Determine identifier
#             if not obj_id:
#                 obj_id=self._tag_id or id(self)
#             self._tag_id=obj_id
#     
#             # Handle default type
#             if not self._tag_default_type or default == True:
#                 self._tag_default_type=tagtype.name
#             
#             # Register object
#             tagtype.addObj(self._tag_id, self)
#     
#             # Init tags structure
#             typedata = self._tag_data.get(tagtype.name or {})
#             typedata['tag_type_name']=tagtype.name
#             typedata['tag_type_ref']=tagtype
#             typedata['tag_data']=Store('tag_data_' + identifier)
#             self._tag_data[tagtype.name]=typedata
#     
#     
#     
#         # API methods (Please use decorators !!!!)
#         def addTag(self, tagname, typename=None, value=None):
#             typedata=self._tag_data[typename or self._tag_default_type]['tag_data']
#             typedata.addKey(tagname, value)
#     
#             tagtype=self._tag_data[typename or self._tag_default_type]['tag_type_ref']
#             return tagtype.getTag(tagname).addObj(self._tag_id)
#     
#         def rmTag(self, tag, typename=None):
#             typedata=self._tag_data[typename or self._tag_default_type]['tag_data']
#             typedata.rmKey(tagname)
#     
#             tagtype=self._tag_data[typename or self._tag_default_type]['tag_type_ref']
#             tagtype.rmTag(tagname).rmObj(self._tag_id)
#     
#         def getTags(self, typename=None):
#             typedata=self._tag_data[typename or self._tag_default_type]['tag_data']
#             return typedata.getTags(tagname, value)
#     
#             #tagtype=self._tag_data[typename or self._tag_default_type]['tag_type_ref']
#             #return tagtype.getTags()
#     
#         def getTag(self, tagname, typename=None):
#             typedata=self._tag_data[typename or self._tag_default_type]['tag_data']
#             return typedata.getTag(tagname)
#     
#             #tagtype=self._tag_data[typename or self._tag_default_type]['tag_type_ref']
#             #typedata=self._tag_data[typename or self._tag_default_type]
#             #return tagtype.getTag(tagname)
#     
#         #def setTagValue(self, tag, value, store=None):
#         #    tag=self.getTag(tag)
#         #    return store.setKeyValue(tag, value)
#     
#         #def getTagValue(self, tag, store=self._tag_default_store):
#         #    tagtype=self.tagtype_ref
#         #    return store.getKeyValue(tag)
#     
#     
#     
#     ################################### POC
#     
#     
#     T=TagManager()
#     tagAuthor=T.addTagStore('author')
#     tagType=T.addTagStore('type')
#     tagDefault=T.addTagStore('tags')
#     
#     
#     # One item !!!!!
#     
#     class workshopmod(Tagged):
#         def __init__(self):
#             #Tagged.__init__(self)
#             self.initTags(self, store=tagAuthor)
#             self.initTags(self, store=tagType)
#             self.initTags(self, store=tagDefault)
#     
#     
#     
#     class modlist(Tagged):
#         def __init__(self):
#             #Tagged.__init__(self)
#             self.initTags(self, 'tags')
#     
#     
#     class mod(Tagged):
#         def __init__(self):
#             #Tagged.__init__(self)
#             self.initTags(self, 'mod')
#             self.initTags(self, 'modlist')
#             self.initTags(self, 'playlist')
#             self.initTags(self, 'tags')
#     
#     
#     workshopmod1.addTag('mrjk', store=tagAuthor)
#     workshopmod2.addTag('tutut', store=tagAuthor)
#     
#     
#     
#     
#     TagManager:
#         addTagType()
#         getTagType('name')
#     
#     
#     tag.getObjs()
#     obj.getTags()
#     