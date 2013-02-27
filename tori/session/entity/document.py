from tori.session.entity.base import Base
from tori.db.document         import document

@document
class Document(Base):
    """
    BaseDocument Session Entity is made to use with a Repository session repository (MongoDB).
    """
    def __init__(self, session_id, key, content, _id=None):
        Base.__init__(self, session_id, key, content)

        self._id = _id
