from passerine.db.entity  import entity
from passerine.db.manager import ManagerFactory

@entity
class Player(object):
    def __init__(self, name, level, team=None):
        self.name  = name
        self.level = level
        self.team  = None

    def __repr__(self):
        attrs = {
            'name':  self.name,
            'team':  self.team,
            'level': self.level
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

sid = Player('Sid', 5)

session = entity_manager.open_session()

# cleanup (for demo-only)
session.driver.collection('player').drop()
session.driver.collection('teams').drop()

# Create an entity
repository = session.repository(Player)
repository.persist(sid)
repository.commit()

# Add more entities
repository.persist(Player('Ramza', 9))
repository.persist(Player('Tsunemori', 6))
repository.commit()

# Query multiple without constrain
result = repository.find()
print('Query multiple entities without constrains (a)\n{}'.format(result))

# Query multiple without constrain
query  = repository.new_criteria('p')
result = repository.find(query)
print('Query multiple entities without constrains (b)\n{}'.format(result))

#query = repository.new_criteria()

# Query multiple with primitive value
query = repository.new_criteria('p')
query.expect('p.name = "Sid"')

result = repository.find(query)
print('Search multiple entities with primitive value.\n{}'.format(result))

# Query multiple with parameters
query = repository.new_criteria('p')
query.expect('p.name = :name')
query.define('name', 'Sid')

result = repository.find(query)
print('Search multiple entities with parameters (new criteria).\n{}'.format(result))

# Query multiple with the same criteria but different parameters
query.define('name', 'Tsunemori')
result = repository.find(query)
print('Search multiple entities with parameters. (used criteria).\n{}'.format(result))

# Range-query multiple
query = repository.new_criteria('p')
query.expect('p.level >= 5')
query.expect('p.level <= 6')
result = repository.find(query)
print('Range-query multiple with.\n{}'.format(result))

# Index-query multiple
query = repository.new_criteria('p')
query.expect('p.level IN :expected_level')
query.define('expected_level', (6, 9))
result = repository.find(query)
print('Index-query multiple.\n{}'.format(result))

# REGEX-query multiple
query = repository.new_criteria('p')
query.expect('p.name LIKE :name')
query.define('name', '^Ra')
result = repository.find(query)
print('REGEX-query multiple.\n{}'.format(result))
