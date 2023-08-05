import os
import types
from itertools import zip_longest

import requests
from addict import Dict

from pyqalx.core.encryption import QalxEncrypt

from pyqalx.core.errors import QalxAPIResponseError, QalxError, QalxQueueError


class QalxAddict(Dict):
    """
    A qalx subclass of addict.Dict.  Enables us to have entities that operate
    like normal dicts, but allow dot notation for all the keys.  Ensures that
    if something is passed to it that is already an instance of QalxEntity
    that we don't mutate the type to a QalxAddict instance
    """

    @classmethod
    def _hook(cls, item):
        """
        Ensure that if the `item` is an instance of QalxEntity (a dict), that
        we don't mutate the type to be an addict.Dict class.  We want to
        preserve the type and the QalxEntity instance has already gone through
        addict.Dict to allow dot notation lookup
        """
        if not isinstance(item, QalxEntity):
            item = super(QalxAddict, cls)._hook(item)
        return item


class BaseQalxEntity(dict):
    """
    The base class for all QalxEntity instances.  Operates like a normal `dict`
    but utilises `addict.Dict` to allow a user to do dot notation lookup of
    all keys recursively.
    """

    def __init__(self, *args):
        super(BaseQalxEntity, self).__init__(*args)

        for key, value in self.items():
            # Ensure that `__setitem__` is called for all top level keys.  This
            # will enable dot notation lookup to work.
            self[key] = value

    @staticmethod
    def _addict(value):
        """
        Handles turning the value into a QalxAddict subclass. Will only attempt
        conversion if value is an instance of dict and is not already an instance
        of QalxEntity, or if it is a list/tuple in which case it iterates it
        and attempts conversion on all elements that are a dict and not an
        instance of QalxEntity in which case it will already have dot notation
        available
        """

        def _do_conversion(_value):
            return isinstance(_value, dict) and not isinstance(
                _value, QalxEntity
            )

        if _do_conversion(value):
            value = QalxAddict(value)
        elif isinstance(value, (list, tuple)):
            value = [QalxAddict(x) if _do_conversion(x) else x for x in value]
        return value

    def _reserved_keys(self):
        """
        A list of reserved keys for this entity.  Keys that are listed in here
        will never be assigned to the dict value when setting the attribute.
        i.e. if `_reserved_keys` returns ["_broker_client"] then doing
        `myentity._broker_client = None` would set the attribute of
        `_broker_client` but NOT the dict key.  Only applies for top level
        dict keys
        """
        return []

    def __setitem__(self, key, value):
        """
        Ensure that the appropriate attribute is set for `key`.
        Takes advantage of dict mutability so that if a user does
         `myentity.data.nested.value = 5` it will update the attribute
        and the dict key.  The same goes for if the user does
        `myentity['data']['nested']['value'] = 5`
        """
        value = self._addict(value)
        super(BaseQalxEntity, self).__setitem__(key, value)
        # Now that the dict has been updated with an addict value, ensure
        # that the attribute is kept in sync.  Ensure that we don't override
        # any builtins.  This means a user will have to do `entity['items']`
        # if they want to access `items` - which keeps `entity.items()` working
        # like the baseclass
        if not isinstance(
            getattr(self, key, None),
            (types.BuiltinMethodType, types.MethodType),
        ):
            setattr(self, key, value)

    def __setattr__(self, key, value):
        """
        Ensures that if a user updates a root level attribute
        (i.e. myentity.meta = {"new": "meta"}) that the dict key is updated
        to keep the dict and attribute values in sync.  Ignores specific
        reserved keys which are specifically set on the instance.
        """
        super(BaseQalxEntity, self).__setattr__(key, value)
        if key not in self._reserved_keys():
            sentinel = object()
            if self.get(key, sentinel) != value:
                self[key] = value


class QalxListEntity(BaseQalxEntity):
    """
    Simple wrapper around a pyqalxapi_dict so we can keep extra keys
    on the API list response.  Instantiates each entity in `data` to the
    correct QalxEntity subclass.
    """

    _data_key = "data"

    def __init__(self, pyqalxapi_list_response_dict, **kwargs):
        self.child = kwargs.pop("child")
        self._key_file = kwargs.pop("keyfile", None)
        super(QalxListEntity, self).__init__(pyqalxapi_list_response_dict)

        if (
            self._data_key not in pyqalxapi_list_response_dict
            or not isinstance(
                pyqalxapi_list_response_dict[self._data_key], list
            )
        ):
            raise QalxAPIResponseError(
                "Expected `{0}` key in "
                "`pyqalxapi_list_response_dict` and for"
                " it to be a list".format(self._data_key)
            )

    def _reserved_keys(self):
        reserved_keys = super(QalxListEntity, self)._reserved_keys()
        reserved_keys += ["_key_file", "child"]
        return reserved_keys

    def __setitem__(self, key, value):
        """
        Ensures that if `key == self._data_key` that all the entities on the
        data key are instantiated to be `self.child` entities.
        """
        if key == self._data_key:
            kwargs = {}
            if self._key_file is not None:
                kwargs = {"keyfile": self._key_file}
            value = [self.child(x, **kwargs) for x in value]
        super(QalxListEntity, self).__setitem__(key, value)


class AggregationResult(QalxListEntity):
    """
    Class for aggregation result responses from the API
    """


class QalxEntity(BaseQalxEntity):
    """Base class for qalx entities_response.

    QalxEntity children need to be populated with either a
    `requests.models.Response` which is the type returned by the methods
    on `pyqalxapi.api.PyQalxAPI` or with a `dict`.

    Entities can behave either like a dict or attribute lookups can be used
    as getters/setters

    >>> class AnEntity(QalxEntity):
    ...     pass
    >>> c = AnEntity({"guid":"123456789", "info":{"some":"info"}})
    >>> # dict style lookups
    >>> c['guid']
    '123456789'
    >>> # attribute style lookups
    >>> c.guid
    '123456789'


    :param pyqalxapi_dict: a 'dict' representing a qalx entity object to
        populate the entity
    :type pyqalxapi_dict: dict
    """

    entity_type: str

    @classmethod
    def _chunks(cls, _iterable, chunk_size, fillvalue=None):
        """
        Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        Taken from the itertools documentation
        """
        args = [iter(_iterable)] * chunk_size
        return zip_longest(fillvalue=fillvalue, *args)

    @classmethod
    def pluralise(cls):
        """
        Pluralises the entity type
        """
        vowels = {"a", "e", "i", "o", "u", "y"}
        singular = cls.entity_type
        plural = singular + "s"
        if len(singular) > 1 and singular.endswith("y"):
            if singular[-2] not in vowels:
                plural = singular[:-1] + "ies"
        return plural


class QalxFileEntity(QalxEntity):
    _file_bytes = None
    _file_key = "file"

    def __init__(self, *args, **kwargs):
        """
        QalxFileEntity subclasses can be provided with a `keyfile` kwarg.
        This gets set on the instance of the entity and will allow for seamless
        decryption of files
        """
        self._key_file = kwargs.pop("keyfile", None)
        super(QalxFileEntity, self).__init__(*args, **kwargs)

    def _reserved_keys(self):
        reserved_keys = super(QalxFileEntity, self)._reserved_keys()
        reserved_keys += ["_key_file", "_file_bytes"]
        return reserved_keys

    def read_file(self):
        """
        If this Item contains a file, will read the file data and cache it
        against the Item.

        :param key_file:    The path to the encryption key to be used for
                            decrypting the file data. If it is not provided
                            and the data was encrypted, the data will be read
                            in the encrypted format
        :return:    The content of the URL as a bytes object.  Accessible from
                    the `_file_bytes` attribute
        :raises: pyqalx.errors.QalxError
        """
        if not self.get(self._file_key):
            raise QalxError("Item doesn't have file data.")
        else:
            response = requests.get(url=self[self._file_key]["url"])
            if response.ok:
                file_bytes = response.content
                if (
                    self[self._file_key].get("keyfile") is not None
                    and self._key_file is not None
                ):
                    qalx_encrypt = QalxEncrypt(self._key_file)
                    file_bytes = qalx_encrypt.decrypt(file_bytes)
                self._file_bytes = file_bytes
                return self._file_bytes
            else:
                raise QalxError(
                    "Error with file retrieval: \n\n" + response.text
                )

    def save_file_to_disk(self, filepath, filename=None):
        """
        If this Item contains a file, will read the file from the URL (or from
        the cached bytes on the instance) and save the file to disk.  Provide
        an optional `filename` argument if you don't want to use the same
        filename as the one stored on the Item

        :param filepath: The path where this file should be saved
        :type filepath: str
        :param filename: The optional name of this file. Defaults to the name
            of the file on the instance
        :type filename: str
        :param key_file:    The path to the encryption key to be used for
                            decrypting the file data. If it is not provided
                            and the data was encrypted, the data will be read
                            in the encrypted format
        :type key_file:     str
        :raises: pyqalx.errors.QalxError
        """
        if filename is None:
            filename = self[self._file_key]["name"]
        if self._file_bytes is None:
            self.read_file()
        _filepath = os.path.join(filepath, filename)
        with open(_filepath, "wb") as f:
            f.write(self._file_bytes)
        return _filepath


class QalxQueueableEntity(QalxEntity):
    """
    A mixin which allows an entity to be sumitted to queue
    """

    @classmethod
    def add_to_queue(cls, payload, queue, children=False, **message_kwargs):
        """
        Submits an entity, entity guid or list of entities/entity guids
        to the given queue
        :param payload:subclassed instance of ~entities.entity.QalxEntity,
        a guid, or a list containing a combination of both
        :param queue: An instance of ~entities.queue.Queue
        Usage:
        :type queue:~entities.queue.Queue
        :param children:Whether we are submitting the child entities to the
        queue rather than the given entity
        :type children: bool
        Example usage for an Item
        Item.add_to_queue(item, queue)
        Item.add_to_queue(item.guid, queue)
        Item.add_to_queue([item, item.guid], queue)
        """
        entity_type = cls.entity_type
        if children:
            #  Get the children off this entity and submit them to the queue
            if not hasattr(cls, "child_entity_class"):
                raise QalxQueueError(
                    f"`{cls}` is not an entity that " f"has children."
                )
            if not isinstance(payload, cls):
                raise QalxQueueError(
                    f"Expected payload of type `{cls}"
                    f"` when calling `{cls.__name__}.add_to_queue` "
                    f"with `children=True`. "
                    f"Got `{type(payload)}`."
                )
            # SQS needs the guid as a string - not UUID
            message_kwargs[f"parent_{entity_type}_guid"] = str(payload["guid"])
            entity_type = cls.child_entity_class.entity_type
            payload = list(payload[cls.child_entity_class.pluralise()].values())
        return queue._send_message(
            payload=payload, entity_type=entity_type, **message_kwargs
        )
