from pyqalx.core.adapters.adapter import (
    QalxUnpackableAdapter,
    QalxValidateBlueprintAdapter,
)
from pyqalx.core.entities import Set


class QalxSet(QalxValidateBlueprintAdapter, QalxUnpackableAdapter):
    _entity_class = Set
    child_entity_class = Set.child_entity_class

    def add(self, items, meta=None, blueprint_name=None, **kwargs):
        """
        When adding a `Set` ensure that the items posted to the api are in the
        format {<key>: <Item instance>}

        :param items: A dictionary of Items to create on the set
        :type items: dict
        :param meta: A dictionary of metadata to store on this set
        :type meta: dict
        :param blueprint_name: An optional blueprint
         name to use if you want to validate this set against an existing Blueprint
        :type blueprint_name: str
        :return: A newly created `Set` instance

        """
        return super(QalxSet, self).add(
            items=items, blueprint_name=blueprint_name, meta=meta, **kwargs
        )
