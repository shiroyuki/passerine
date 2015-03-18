5. Updating, Deleting and Handling Transactions (Sessions)
##########################################################

Similar to `Sessions in SQLAlchemy <http://docs.sqlalchemy.org/en/latest/orm/session.html>`_.

In the most general sense, the session establishes all conversations with the
database and represents a “holding zone” for all the objects which you’ve loaded
or associated with it during its lifespan. It provides the entrypoint to acquire
a :class:`passerine.db.repository.Repository` object, which sends queries to the
database using the current database connection of the session (:class:`passerine.db.session.Session`),
populating result rows into objects that are then stored in the session, inside
a structure called the identity map (internally being the combination of "the
record map" and "the object ID map") - a data structure that maintains unique
copies of each object, where “unique” means “only one object with a particular
primary key”.

The session begins in an essentially stateless form. Once queries are issued or
other objects are persisted with it, it requests a connection resource from an
manager that is associated with the session itself. This connection represents
an ongoing transaction, which remains in effect until the session is instructed
to commit.

All changes to objects maintained by a session are tracked - before the database
is queried again or before the current transaction is committed, it flushes all
pending changes to the database. This is known as **the Unit of Work pattern**.

When using a session, it’s important to note that the objects which are associated
with it are **proxy objects** (:class:`passerine.db.common.ProxyObject`) to the
transaction being held by the session - there are a variety of events that will
cause objects to re-access the database in order to keep synchronized. It is
possible to “detach” objects from a session, and to continue using them, though
this practice has its caveats. It’s intended that usually, you’d re-associate
detached objects with another Session when you want to work with them again, so
that they can resume their normal task of representing database state.

Supported Operations
====================

=================== =====================
Supported Operation Supported Version
=================== =====================
Persist             2.1
Delete              2.1
Refresh             2.1
Merge               No plan at the moment
Detach              No plan at the moment
=================== =====================

Open a Session
==============

As you might guess from :doc:`02-create-entity`, Passerine always requires the
code to open a session by::

    session = entity_manager.open_session()

Getting Started (again)
=======================

Then, try to query a player called **"Sid"**, we created in :doc:`02-create-entity`
with :class:`passerine.db.repository.Repository`::

    repo = session.collection(Player)

    query = repo.new_criteria('c')
    query.expect('c.name = :name')
    query.define('name', 'Sid')

    player = repo.find(query)

    # For demonstration only
    print('Sid/level: {}'.format(player.level))

The output should show::

    Sid/level: 5

Update an Entity
================

Suppose we want to update his level::

    player.level = 99
    repo.persist(player)

Delete an Entity
================

Suppose we want to delete the entity::

    session.delete(player)

.. note::

    Until you commit the changes, other queries still can return entities you
    mark as deleted.

Commit Changes
==============

Once I am satisfied with changes, commit the changes with::

    repo.commit()

or::

    session.flush()

.. note::

    We will stick with ``session.flush()`` as ``repo.commit()`` is just an alias to ``session.flush()``.

.. note::

    To discard all changes at any points, just close the session (mentioned later in this section).

Refresh/revert Changes on One Entity
====================================

Or, refresh ``player``::

    session.refresh(player)

Then, if ``player`` is either **persisted** or **deleted**, to flush/commit the
change, simply run::

    session.flush()

Close a Session
===============

Closing a session is to end the session or discard all changes to the session.
You can simply close the session by::

    entity_manager.close_session(session)

Handle a Session in the Context
===============================

To ensure all sessions are closed properly, you can open session as a context manager by doing this::

    with entity_manager.session() as session:
        ... # do whatever
    # session closed

Drawbacks Introduced by Either MongoDB or Passerine
===================================================

#. Even though MongoDB does not support transactions, like some relational database
   engines, such as, InnoDB, Passerine provides software-based transactions. However,
   as mentioned earlier, Passerine **does not provide roll-back operations**.
#. **Merging** and **detaching** operations are currently not supported in 2013
   unless someone provides the supporting code.
#. Any querying operations cannot find any uncommitted changes.
