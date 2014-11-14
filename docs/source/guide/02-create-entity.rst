2. Create a New Entity
######################

In the previous step, we have an entity manager (``entity_manager``) and two entity classes (``Player`` and ``Team``).
Now, we are going to create a new entity.

Let's create **one player**.

.. code-block:: python

    sid = Player('Sid', 5)

    session = entity_manager.open_session()
    
    repository = session.repository(Player)
    repository.persist(sid)
    repository.commit()

From the code, ``sid = Player('Sid')`` is to create an object.

The rest are pretty simple.

#. We open a DB (pseudo) session with ``open_session()``,
#. find the corresponding repository, referred as ``repository``,
#. tell the repository to push the new object on commit with ``persist()``,
#. and finally commit the change to the database.

.. note::

    Alternatively, you may forget ``repository`` by using ``session`` directly
    by replacing everything about ``repository`` with the following code.
    
    .. code-block:: python
    
        session.persist(sid)
        session.flush()
    
    where the session's ``persist`` and ``commit`` are the same as the repository's
    ``persist`` and ``flush`` respectively. **For the sake of tutorial, we will
    keep using the repository approach.**

.. warning:: The database session is pseudo for unsupported databases.

.. note::

    The way we use ``open_session()`` here is to open an unsupervised session. The session connection cannot be closed
    by the supervising entity manager but the connection is still closed as soon as the process is terminated.

After this process, you can verify with MongoDB CLI (``mongo sample_db``) by running ``db.player.find()``. You should
be able to see the result on the screen like the following (except ``_id``).

.. code-block:: javascript

    {
        "_id" : ObjectId("..."),
        "name" : "Sid",
        "level": 5,
        "team" : null
    }