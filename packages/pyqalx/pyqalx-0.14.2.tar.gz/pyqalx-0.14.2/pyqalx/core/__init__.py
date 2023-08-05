"""
Sessions
~~~~~~~~~~~~~~~~~~~

The best way to interface between entities and qalx is with the `session` object.
This has a series of helper methods to interface with the API using entity
specific `adapters`

.. _qalxsession:

.. automodule:: pyqalx.core.session
    :members:

Adapters
~~~~~~~~

Adapters are how a `session` interfaces with the API.  These won't typically
get accessed directly - instead the helper properties on the `session` should be
used.

.. automodule:: pyqalx.core.adapters.blueprint
     :members:

.. automodule:: pyqalx.core.adapters.bot
     :members:

.. automodule:: pyqalx.core.adapters.group
     :members:

.. automodule:: pyqalx.core.adapters.item
     :members:

.. automodule:: pyqalx.core.adapters.queue
     :members:

.. automodule:: pyqalx.core.adapters.set
     :members:

.. automodule:: pyqalx.core.adapters.worker
     :members:


Entities
~~~~~~~~
Root entities - these are children of ``dict`` but with special methods

.. _bot_entity:
.. automodule:: pyqalx.core.entities.bot
    :members:

.. _qalx_entity:
.. automodule:: pyqalx.core.entities.entity
    :members:

.. _group_entity:
.. automodule:: pyqalx.core.entities.group
    :members:

.. _item_entity:
.. automodule:: pyqalx.core.entities.item
    :members:

.. _queue_entity:
.. automodule:: pyqalx.core.entities.queue
    :members:

.. _set_entity:
.. automodule:: pyqalx.core.entities.set
    :members:

.. _worker_entity:
.. automodule:: pyqalx.core.entities.worker
    :members:

.. _blueprint_entity:
.. automodule:: pyqalx.core.entities.blueprint
    :members:


Logging
~~~~~~~

.. automodule:: pyqalx.core.log
    :members:


Signals
~~~~~~~

.. automodule:: pyqalx.core.signals
    :members:

Errors
~~~~~~

.. automodule:: pyqalx.core.errors
    :members:



"""
