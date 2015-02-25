4. Associations and Relational Mappings
#######################################

Usually data from different collections are related and may co-exist. As the result, even though some database
softwares do not allow associations, Passerine allows the software-based relational mapping. This ORM supports
all types of relational mapping either unidirectionally or bidirectionally.

Passerine ORM utilizes two patterns to implement association.

* Decorators (AKA annotations) to define associations.
* Lazy loading to load data when it is requested.
* Proxy object as direct result of lazy loading.

In general, the decorator :meth:`passerine.db.mapper.link` is used to define association by mapping decorated
fields to another classes by primary key (or object ID). The ID-to-object happens automatically during data
mapping.

Types of Associations
=====================

For the sake of the simplicity of this chapter, all examples are assumed to
be in the module ``sampleapp.model``, and begin with::

    from passerine.db.entity import entity
    from passerine.db.mapper import link, AssociationType as t, CascadingType as c

One-to-one
----------

Suppose there are two entities: ``Owner`` and ``Restaurant``,
**one-to-one associations** imply the relationship between two entities as
described in the following UML::

     Owner (1) ----- (1) Restaurant

Unidirectional
~~~~~~~~~~~~~~

UML::

    Owner (1) <--x- (1) Restaurant

Suppose we have two classes: ``Owner`` and ``Restaurant``, where ``Restaurant``
has the one-to-one unidirectional relationship with ``Owner``.

.. code-block:: python

    @entity
    class Owner(object):
        def __init__(self, name):
            self.name  = name

    @link(
        target      = 'sampleapp.model.Owner',
        mapped_by   = 'owner',
        association = t.ONE_TO_ONE
    )
    @entity
    class Restaurant(object):
        def __init__(self, name, owner):
            self.name  = name
            self.owner = owner

where the sample of the stored documents will be:

.. code-block:: javascript

    // collection: owner
    {'_id': 'o-1', 'name': 'siamese'}

    // collection: restaurant
    {'_id': 'rest-1', 'name': 'green curry', 'owner': 'o-1'}

.. tip::

    To avoid the issue with the order of declaration, the full namespace in
    string is recommended to define the target class. However, the type
    reference can also be. For example, ``@link(target = Owner, ...)``.

Bidirectional
~~~~~~~~~~~~~

UML::

    Owner (1) <---> (1) Restaurant

Now, let's allow ``Owner`` to have a reference back to ``Restaurant`` where the
information about the reference is not kept with ``Owner``. So, the

.. code-block:: python

    @link(
        target      = 'sampleapp.model.Restaurant'
        inverted_by = 'owner',
        mapped_by   = 'restaurant',
        association = t.ONE_TO_ONE
    )
    @entity
    class Owner(object):
        def __init__(self, name, restaurant):
            self.name       = name
            self.restaurant = restaurant

where the the stored documents will be the same as the previous example.

``inverted_by`` means this class (``Owner``) maps ``Restaurant`` to the property
*restaurant* where the value of the property *owner* of the corresponding entity
of Restaurant must equal the *ID* of this class.

.. note::

    The option ``inverted_by`` only maps ``Owner.restaurant`` to ``Restaurant``
    virtually but the reference is stored in the **restaurant** collection.

Many-to-one
-----------

Suppose a ``Customer`` can have many ``Reward``'s as illustrated::

    Customer (1) ----- (0..n) Reward

Unidirectional
~~~~~~~~~~~~~~

UML::

    Customer (1) <--x- (0..n) Reward

.. code-block:: python

    @entity
    class Customer(object):
        def __init__(self, name):
            self.name    = name

    @link(
        target      = 'sampleapp.model.Customer',
        mapped_by   = 'customer',
        association = t.MANY_TO_ONE
    )
    @entity
    class Reward(object):
        def __init__(self, point, customer):
            self.point    = point
            self.customer = customer

where the data stored in the database can be like this:

.. code-block:: javascript

    // collection: customer
    {'_id': 'c-1', 'name': 'panda'}

    // collection: reward
    {'_id': 'rew-1', 'point': 2, 'customer': 'c-1'}
    {'_id': 'rew-2', 'point': 13, 'customer': 'c-1'}

.. _manual_orm_associations_m-1_bidirectional:

Bidirectional
~~~~~~~~~~~~~

UML::

    Customer (1) <---> (0..n) Reward

Just change ``Customer``.

.. code-block:: python

    @link(
        target      = 'sampleapp.model.Reward',
        inverted_by = 'customer',
        mapped_by   = 'rewards',
        association = t.ONE_TO_MANY
    )
    @entity
    class Customer(object):
        def __init__(self, name, rewards):
            self.name    = name
            self.rewards = rewards

where the property *rewards* refers to a list of rewards but the stored data
remains unchanged.

.. note:: This mapping is equivalent to a **bidirectional one-to-many mapping**.

One-to-many
-----------

Let's restart the example from the many-to-one section.

Unidirectional with Built-in List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The one-to-many unidirectional mapping takes advantage of the built-in list.

UML::

    Customer (1) -x--> (0..n) Reward

.. code-block:: python

    @link(
        target      = 'sampleapp.model.Reward',
        mapped_by   = 'rewards',
        association = t.ONE_TO_MANY
    )
    @entity
    class Customer(object):
        def __init__(self, name, rewards):
            self.name    = name
            self.rewards = rewards

    @entity
    class Reward(object):
        def __init__(self, point):
            self.point = point

where the property ``rewards`` is a unsorted iterable list of ``Reward`` objects
and the data stored in the database can be like this:

.. code-block:: javascript

    // collection: customer
    {'_id': 'c-1', 'name': 'panda', 'reward': ['rew-1', 'rew-2']}

    // collection: reward
    {'_id': 'rew-1', 'point': 2}
    {'_id': 'rew-2', 'point': 13}

.. warning::

    As there is no way to enforce relationships with built-in functionality of
    MongoDB and there will be constant checks for every write operation, it is
    not recommended to use unless it is for **reverse mapping** via the option
    ``inverted_by`` (see below for more information).

    Without a proper checker, which is not provided for performance sake, this
    mapping can be used like the **many-to-many join-collection mapping**.

Bidirectional
~~~~~~~~~~~~~

See :ref:`Many-to-one Bidirectional Association <manual_orm_associations_m-1_bidirectional>`.

Many-to-many
------------

Suppose there are ``Teacher`` and ``Student`` where students can have many
teachers and vise versa::

    Teacher (*) ----- (*) Student

Similar other ORMs, the many-to-many mapping uses the corresponding join
collection.

Unidirectional with Join Collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UML::

    Teacher (*) <--x- (*) Student

.. code-block:: python

    @entity('teachers')
    class Teacher(object):
        def __init__(self, name):
            self.name = name

    @link(
        mapped_by   = 'teachers',
        target      = Teacher,
        association = AssociationType.MANY_TO_MANY,
        cascading   = [c.DELETE, c.PERSIST]
    )
    @entity('students')
    class Student(object):
        def __init__(self, name, teachers=[]):
            self.name     = name
            self.teachers = teachers

where the stored data can be like the following example:

.. code-block:: javascript

    // db.students.find()
    {'_id': 1, 'name': 'Shirou'}
    {'_id': 2, 'name': 'Shun'}
    {'_id': 3, 'name': 'Bob'}

    // db.teachers.find()
    {'_id': 1, 'name': 'John McCain'}
    {'_id': 2, 'name': 'Onizuka'}

    // db.students_teachers.find() // -> join collection
    {'_id': 1, 'origin': 1, 'destination': 1}
    {'_id': 2, 'origin': 1, 'destination': 2}
    {'_id': 3, 'origin': 2, 'destination': 2}
    {'_id': 4, 'origin': 3, 'destination': 1}

Bidirectional
~~~~~~~~~~~~~

Implemented in Tori 2.1 (See the usage from https://github.com/shiroyuki/Tori/issues/27).

.. TODO:: update this section

Options for Associations
========================

The decorator :meth:`passerine.db.mapper.link` has the following options:

=========== ======================================================================================================
Option      Description
=========== ======================================================================================================
association the type of associations (See :class:`passerine.db.mapper.AssociationType`.)
cascading   the list of allowed cascading operations (See :doc:`06-cascading` :class:`passerine.db.mapper.CascadingType`.)
inverted_by the name of property used where **enable the reverse mapping if defined**
mapped_by   the name of property to be map
read_only   the flag to disable property setters (only usable with :class:`passerine.db.common.ProxyObject`.)
target      the full name of class or the actual class
=========== ======================================================================================================

How to make a join query
========================

.. versionadded:: 3.0

From the customer-reward example, if we want to find all rewards of a particular
user, the query will be::

    query = reward_repository.new_criteria('r')
    query.join('r.customer', 'c')
    query.expect('c.name = "Bob"')

    rewards = reward_repository.find(query)


