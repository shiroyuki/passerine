3. Find entities (Basic)
########################

Previously, we added an entity. Now, we just need to find it properly.

However, just before we move onto the next step, let's add more Player entities.

.. code-block:: python

    # Add more entities
    repository.persist(Player('Ramza', 9))
    repository.persist(Player('Tsunemori', 6))
    repository.commit()

Find many entities without constrains
=====================================

Suppose we want to retrieve everyone. There are two ways you can do it.

First, just invoke the ``find`` method of ``repository``.

.. code-block:: python

    result = repository.find()

Or alternatively, you can create a new :class:`passerine.db.query.Query` via ``repository``.

.. code-block:: python

    query = repository.new_criteria('p')

    result = repository.find(query)

You should then see the same output (``result``) like the following::

    [<Player {'level': 5, 'name': 'Sid', 'team': None}>, <Player {'level': 6, 'name': 'Tsunemori', 'team': None}>, <Player {'level': 9, 'name': 'Ramza', 'team': None}>]

.. warning::

    :class:`passerine.db.query.Query` must always be instantiated via :class:`passerine.db.repository.Repository`.
    Please do not try to instantiate the **Query** class directly.

Find many entities with constrains
==================================

Suppose we want to retrieve the information of the player named "Sid". There are two ways you can do it.

Hand-coded expectation
----------------------

First, just hand-code the expected value.

.. code-block:: python

    query = repository.new_criteria('p')
    query.expect('p.name = "Sid"')

    result = repository.find(query)

``query = repository.new_criteria('p')`` is to instantiate a query object (:class:`passerine.db.query.Query`) where
the alias of the expected entitiy is ``p``. Then, ``query.expect('p.name = "Sid"')`` set the expectation that the
attribute ``name`` of the expected entities must be equal to ``Sid``. ``result = repository.find(query)`` will perform
the query with the specification defined in ``query``. If you execute the code, you should see the output (``result``) like this::

    [<Player {'level': 5, 'name': 'Sid', 'team': None}>]

.. note::

    The syntax for the expectation is ironically similar to SQL and DQL (Doctrine Query Language). It is by design to
    generalize the interface between different types of drivers.

Parameterized expectation (exact match)
---------------------------------------

However, the previous ``query`` is not reusable with the dynamic data. We will create the Query object with
**parameters** to allow use to reuse the same query object for different parameters.

.. code-block:: python

    query = repository.new_criteria('p')
    query.expect('p.name = :name')
    query.define('name', 'Sid')

    result = repository.find(query)

In this snippet, you will see that in ``query.expect('p.name = :name')``, ``:name`` replaces ``"Sid"`` and
``query.define('name', 'Sid')`` defines the value of the parameter ``name``. This is equivalent to
``query.expect('p.name = "Sid"')`` as you will see the same output (``result``)::

    [<Player {'level': 5, 'name': 'Sid', 'team': None}>]

However, without recreating the Query object, if I re-define the parameter ``name`` with ``Tsunemori`` by adding::

    query.define('name', 'Tsunemori')

you will now get the different result::

    [<Player {'level': 6, 'name': 'Tsunemori', 'team': None}>]

.. note::

    This is the recommended way to query.

Parameterized expectation (range)
---------------------------------

To do range search, just like the previous examples, you can either hand-code the expectation or rely on the
parameterization. The following example uses the latter::

    # Range-query multiple
    query = repository.new_criteria('p')
    query.expect('p.level >= :min')
    query.expect('p.level <= :max')
    query.define('min', 5)
    query.define('max', 6)

    result = repository.find(query)

And ``result`` becomes::

    [
        <Player {'level': 5, 'name': 'Sid', 'team': None}>,
        <Player {'level': 6, 'name': 'Tsunemori', 'team': None}>
    ]

Parameterized expectation (in-set)
----------------------------------

To do in-set search, unlike the previous examples, you can only rely on the parameterization. For example::

    query = repository.new_criteria('p')
    query.expect('p.level IN :expected_level')
    query.define('expected_level', (6, 9)) # or [6, 9]

    result = repository.find(query)

And ``result`` becomes::

    [
        <Player {'level': 9, 'name': 'Ramza', 'team': None}>,
        <Player {'level': 6, 'name': 'Tsunemori', 'team': None}>
    ]