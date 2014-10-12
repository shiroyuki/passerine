from passerine.db.entity  import entity
from passerine.db.manager import ManagerFactory

@entity
class Player(object):
    def __init__(self, name, team=None):
        self.name = name
        self.team = None

@entity('teams')
class Team(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location

manager_factory = ManagerFactory()
manager_factory.set('default', 'mongodb://localhost/sample_db')

entity_manager = manager_factory.get('default')

sid = Player('Sid')

session = entity_manager.open_session()

# cleanup
#session.driver.api

repository = session.repository(Player)
repository.persist(sid)
repository.commit()

