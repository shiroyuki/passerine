Change Logs
###########

Version 1.4
===========

Improvements
------------

ManagerFactory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(Short for :class:`passerine.db.manager.ManagerFactory`)

* The alias-to-endpoint-URL map can be passed to the constructor to simplify the usage.
* Shorten the name of each parameters of the constructor.

.. code-block:: python

    from passerine.db.manager import ManagerFactory

    mf = ManagerFactory(urls = {'default': 'mongodb://localhost/sample'})

    mf.get('default') # -> a Manager object

Others
~~~~~~

* The default parameter of the constructor of an Entity class is now respected.

House Cleaning
--------------

* Made Python 3 (<3.4) the primary target.
* Cleaned up the test folder.
* Simplified the test running procedure.

Version 1.1
===========

- (Support Riak 2.0)

Version 1.0
===========

- A fork of Tori ORM (from Tori 3.0) with lots of little improvements.
