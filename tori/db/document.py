from tori.exception import ODMDocumentIdLocked

class Document(object):
    '''
    Basic document for MongoDB
    '''

    def __init__(self, **attributes):
        for name in attributes:
            self.__dict__[name] = attributes[name]

        self.__dict__['_dirty_attributes'] = []
        self.__dict__['_collection_name']  = self.__class__.__name__.lower()

    @property
    def id(self):
        return self.__dict__['_id'] if '_id' in self.__dict__ else None

    @id.setter
    def id(self, id):
        '''
        Define the document ID if the original ID is not defined.

        :param id: the ID of the document.
        '''
        if '_id' in self.__dict__ and self.__dict__['_id']:
            raise ODMDocumentIdLocked('The ID is locked and cannot be changed.')

        self.__setattr__('_id', id)

    @property
    def collection_name(self):
        return self.__dict__['_collection_name']

    def is_dirty(self, name):
        if name not in self.__dict__:
            raise AttributeError('The attribute "%s" is not found.' % name)

        return name in self._dirty_attributes

    def __setattr__(self, name, value):
        if name == '_id':
            raise ODMDocumentIdLocked('"_id" is a reserved attribute.');

        if name not in self.__dict__['_dirty_attributes']:
            self.__dict__['_dirty_attributes'].append(name)

        object.__setattr__(self, name, value)