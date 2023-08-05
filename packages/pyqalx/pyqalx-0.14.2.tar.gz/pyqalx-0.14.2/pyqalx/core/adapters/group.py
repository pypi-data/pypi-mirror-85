from pyqalx.core.adapters.adapter import QalxUnpackableAdapter
from pyqalx.core.entities import Group


class QalxGroup(QalxUnpackableAdapter):
    _entity_class = Group
    child_entity_class = Group.child_entity_class

    def add(self, sets, meta=None, **kwargs):
        """
        When adding a `Group` ensure that the sets posted to the api are in
        the format {<key>: pyqalx.entities.Set}

        :param sets: A dictionary of Sets to create on the group
        :type sets: dict
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :return: A newly created `Group` instance
        """
        return super(QalxGroup, self).add(sets=sets, meta=meta, **kwargs)

    def get(self, guid, child_fields=None, unpack=False, *args, **kwargs):
        """
        Overrides the parent method because for a group the default behaviour
        is to keep the entity packed
        """
        return super(QalxGroup, self).get(
            guid, child_fields=child_fields, unpack=unpack, *args, **kwargs
        )

    def reload(self, entity, unpack=False, *args, **kwargs):
        """
        Overrides the parent method because for a group the default behaviour
        is to keep the entity packed
        """
        return super(QalxGroup, self).reload(
            entity, unpack=unpack, *args, **kwargs
        )

    def find_one(self, query, unpack=False, **kwargs):
        """
        Overrides the parent method because for a group the default behaviour
        is to keep the entity packed
        """
        return super(QalxGroup, self).find_one(query, unpack=unpack, **kwargs)
