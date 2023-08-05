from pyqalx.core.entities import QalxListEntity
from pyqalx.core.entities.entity import QalxFileEntity, QalxQueueableEntity


class Item(QalxFileEntity, QalxQueueableEntity):
    """An item is the core of qalx.

    They are structured data or a file or some combination of the two. For example:

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> dims = qalx.item.add(data={"height":5, "width":5}, meta={"shape":"square"})
    >>> steel = qalx.item.add(source="path/to/316_datasheet.pdf",
    ...                       data={"rho":8000, "E":193e9},
    ...                       meta={"library":"materials",
    ...                             "family":"steel",
    ...                             "grade":"316"})

    We can then use the ``find_one`` and ``find`` methods to search for items

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> steel_316_item = qalx.item.find_one(meta=["library=materials",
    ...                                           "family=steel",
    ...                                           "grade=316"])
    >>> steels = qalx.item.find(meta="family=steel")
    >>> squares = qalx.item.find(meta="shape=square")
    >>> quads = qalx.item.find(meta="(shape=square|shape=rectangle)")

    We can edit an item once we have retrieved it and save it back to qalx.
    You can either use attribute style getters/setters (my_shape.data.height = 10)
    or key style getters/setters (my_shape['data']['height'] = 10)

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> my_shape = qalx.item.find_one(data=["height=5", "width=5"])
    >>> my_shape.data.height = 10
    >>> my_shape.meta.shape = 'rectangle'
    >>> qalx.item.save(my_shape)
    >>> # If we think that someone else might have edited my_shape we can reload it:
    >>> my_shape = qalx.item.reload(my_shape)
    """

    entity_type = "item"


class ItemAddManyEntity(QalxListEntity):
    _data_key = "items"
