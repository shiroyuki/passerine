from passerine.db.entity  import entity
from passerine.db.manager import ManagerFactory

@entity
class Player(object):
    def __init__(self, name, team=None):
        self.name = name
        self.team = None

    def __repr__(self):
        attrs = {
            'name': self.name,
            'team': self.team
        }

        return '<{} {}>'.format(self.__class__.__name__, attrs)

@entity('teams')
class Team(object):
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __repr__(self):
        attrs = {
            'name': self.name,
            'location': self.location
        }

        return '<{} {}>'.format(self.__class__.__name__, attrs)

manager_factory = ManagerFactory()
manager_factory.set('default', 'mongodb://localhost/sample_db')

entity_manager = manager_factory.get('default')

sid = Player('Sid')

session = entity_manager.open_session()

# cleanup
session.driver.db['player'].drop()
session.driver.db['teams'].drop()

# Create an entity
repository = session.repository(Player)
repository.persist(sid)
repository.commit()

query = repository.new_criteria('p')
query.where('p.name = "sid"')

repository.