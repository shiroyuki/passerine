1. Getting Started
##################

Now, you get through the boring stuff. Let's write some code.

Set Up the Connection and Entity Manager
========================================

.. code-block:: python

    from passerine.db.manager import ManagerFactory
    manager_factory = ManagerFactory()

    # Define the connection URL
    manager_factory.set('default', 'mongodb://localhost/sample_db')

    # Get the "default" entity manager
    entity_manager = manager_factory.get('default')

The first three two is to set up the entity manager factory (``ManagerFactory``).

Then, on the next line, we define the **default** connection to ``mongodb://localhost/sample_database``.

Then, use the entity manager factory to get an instance of the **default** entity manager.

Define an Entity
================

.. note::

    From this section on, **collection** (used by NoSQL DBs), **bucket** (used by distributed DBs) and **table**
    (used by relational DBs) are collectively the same thing for the library.

Now, we have an entity manager to work with. Next, we need to define the data structure. For instance, we define two
entity classes: **Character** and **Team**.

.. code-block:: python

    from passerine.db.entity import entity

    @entity
    class Player(object):
        def __init__(self, name, level, team=None):
            self.name = name
            self.team = None
            self.level = level

        def __repr__(self):
            attrs = {
                'name': self.name,
                'team': self.team,
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

#. ``@entity`` is to define the decorated class as an entity class. If all entities of this class will be
   saved in the collection, named **character**.
#. ``@entity('teams')`` is similar to ``@entity`` except that the name of the destination collection is **teams**.
#. The constructor must never take an identifier (e.g. ``id`` or ``_id``) as a parameter.
#. The name of the parameters of the constructor must be the same as the property.

.. note::

    Currently, data-object mapping is very straight forward. If the given data is

    .. code-block:: javascript

        // mongodb: sample_db.teams
        team_raw_data = {
            '_id':       123,
            'name':     'SEED 8',
            'location': 'Wakayama, Japan'
        }

    then, the data mapper will try to do somthing similar to the following code:

    .. code-block:: python

        team_entity = Team(
            name     = team_raw_data['name'],
            location = team_raw_data['location'],
        )
        team_entity.id = team_raw_data['_id']

    The proper data mapping mechanism will be introduced in later releases.

You may use a property getter or setter to restrict the access to the property if needed.

Now, we have **Entity** classes and a working entity manager. What can we do next?