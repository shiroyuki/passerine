Find entities
#############

Previously, we added an entity. Now, we just need to find it properly.

However, just in case, let's add more Player entities.

.. code-block:: python

    # Add more entities
    repository.persist(Player('Ramza'))
    repository.persist(Player('Tsunemori'))
    repository.commit()

Suppose we retrieve the information of the player named "Sid". There are two ways you can do it.

First, just hard-code the expected value.

.. code-block:: python

    query = repository.new_criteria('p')
    query.expect('p.name = "Sid"')

    result = repository.find(query)
    print(result)

``query = repository.new_criteria('p')`` is to instantiate a query object (:class:`passerine.db.query.Query`) where
the alias of the expected entitiy is ``p``. (Please do not try to instantiate the class directly.) Then,
``query.expect('p.name = "Sid"')`` set the expectation that the attribute ``name`` of the expected entities must be
equal to ``Sid``. ``result = repository.find(query)`` will perform the query with the specification defined in
``query``. If you execute the code, you should see the output like this::

    [<Player {'name': 'Sid', 'team': None}>]

.. note::

    The syntax for the expectation is ironically similar to SQL and DQL (Doctrine Query Language). It is by design to
    generalize the interface between different types of drivers.

However, the previous ``query`` is not reusable with the dynamic data. We will create the Query object with
**parameters** to allow use to reuse the same query object for different parameters.

.. code-block:: python

    query = repository.new_criteria('p')
    query.expect('p.name = :name')
    query.define('name', 'Sid')

    result = repository.find(query)
    print(result)

In this snippet, you will see that in ``query.expect('p.name = :name')``, ``:name`` replaces ``"Sid"`` and
``query.define('name', 'Sid')`` defines the value of the parameter ``name``. This is equivalent to
``query.expect('p.name = "Sid"')`` as you will see the same output::

    [<Player {'name': 'Sid', 'team': None}>]

However, without recreating the Query object, if I re-define the parameter ``name`` with ``Tsunemori`` by adding::

    query.define('name', 'Tsunemori')

you will now get the different result::

    [<Player {'name': 'Tsunemori', 'team': None}>]

.. note::

    This is the recommended way to query.