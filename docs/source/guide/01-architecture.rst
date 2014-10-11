Architecture
############

Passerine is primarily designed for non-relational databases. Currently, the
only driver shipped with the library is MongoDB. The next one will be
**Riak 2.0** (a distributed database) and **MySQL** (a relational databases).

There are a few points to highlight.

- The lazy-loading strategy and proxy objects are used to load data wherever
  applicable.
- The ORM uses **the Unit Of Work pattern** as used by:

  - `Hibernate <http://www.hibernate.org/>`_ (Java)
  - `Doctrine <http://www.doctrine-project.org/>`_ (PHP)
  - `SQLAlchemy <http://www.sqlalchemy.org/>`_ (Python)

- By containing a similar logic to determine whether a given entity is new or
  old, the following condition are used:

  - If a given entity is identified with an **object ID**, the given entity will
    be considered as an existing entity.
  - Otherwise, it will be a new entity.

- The object ID cannot be changed via the ORM interfaces.
- The ORM supports cascading operations on deleting, persisting, and refreshing.
- To ensure the performance, heavily rely on **public properties**, which does not
  have leading underscores (``_``) to map between class properties and document
  keys, except the property **id** will be converted to the key **_id**.
- The class design is heavily influenced by dependency injection.

Limitations
===========

- **Cascading operations on persisting** force the ORM to load the data of all
  proxy objects but commiting changes will still be made only if there are changes.
- **Cascading operations on refreshing** force the ORM to reset the data and
  status of all entities, including proxy objects. However, the status of any
  entities marked for deletion will not be reset.

Common for Non-relational or Distributed Databases
--------------------------------------------------

- Sessions cannot merge together.
- **Cascading operations on deleting** forces the ORM to load the whole data
  graph which degrades the performance.

MongoDB Only
------------

- For the MongoDB driver, as MongoDB does not has transaction support like MySQL,
  the ORM has sessions to manage the object graph within the same memory space.
- As **sessions** are not supported by MongoDB, the ORM cannot roll back in case
  that an exception are raisen or a writing operation is interrupted.