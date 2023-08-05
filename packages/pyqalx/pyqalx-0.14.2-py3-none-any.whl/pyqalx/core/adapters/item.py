import concurrent

from pyqalx.core.adapters.adapter import (
    QalxValidateBlueprintAdapter,
    QalxFileAdapter,
)
from pyqalx.core.entities import Item
from pyqalx.core.entities.item import ItemAddManyEntity
from pyqalx.core.errors import QalxError, QalxAPIResponseError


class QalxItem(QalxValidateBlueprintAdapter, QalxFileAdapter):
    _entity_class = Item

    def _validate(
        self,
        data=None,
        source=None,
        file_name="",
        meta=None,
        blueprint_name=None,
        **kwargs,
    ):
        if data is None:
            data = {}
        return super(QalxItem, self)._validate(
            data=data,
            source=source,
            file_name=file_name,
            meta=meta,
            blueprint_name=blueprint_name,
            **kwargs,
        )

    def add(
        self,
        data=None,
        source=None,
        file_name="",
        meta=None,
        blueprint_name=None,
        **kwargs,
    ):
        """
        Adds an `Item` instance that can contain either
        data (as a dict), a file or both.

        :param data: Optional data to store against this Item
        :type data: dict
        :param source: file path or instance of
            StringIO or BytesIO (https://docs.python.org/3/library/io.html)
        :type source: str or `io` object
        :param file_name: input file name. Optional if a file path is given
         for source.  Required if an `io` object
        :type file_name: str
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :param blueprint_name: An optional blueprint name to use to validate
         this item against an existing Blueprint
        :return: A newly created `Item` instance
        """

        return super(QalxItem, self).add(
            data=data,
            source=source,
            file_name=file_name,
            meta=meta,
            blueprint_name=blueprint_name,
            **kwargs,
        )

    def save(
        self, entity, source=None, file_name="", blueprint_name=None, **kwargs
    ):
        """
        Saves an updated existing `Item` instance.
        To remove a file from an `Item` update the entity so that
        `entity['file'] = {}`

        :param entity: The entity that we are saving
        :type entity: An instance of `Item`
        :param source: file path or instance of StringIO or
            BytesIO (https://docs.python.org/3/library/io.html)
        :type source: str or `io` object
        :param file_name: input file name. Optional if a file path is given
            for source.  Required if an `io` object
        :type file_name: str
        :type file_name: str
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :param blueprint_name: An optional blueprint name to use if you want
                               to validate this item against an existing
                               Blueprint
        :type blueprint_name: str
        :return: An updated `Item` instance
        """
        return super(QalxItem, self).save(
            entity=entity,
            source=source,
            file_name=file_name,
            blueprint_name=blueprint_name,
            **kwargs,
        )

    def add_many(self, items, encrypt=True, **kwargs):
        """
        Adds multiple items at once.
        :param items: A list of item data that you want to create.  This can
        be a mixture of non file items and file items. The keys of each item in
        the list should be the same as if a single item were being created via
        the `add` method
        :type items: list
        :param encrypt: Whether the file should be automatically encrypted if
        the KEYFILE is present.  All files are encrypted or not encrypted based
        on this value
        :type encrypt: bool
        :return:
        """
        if not isinstance(items, list):
            raise QalxError("`items` argument must be a list")
        headers = {"qalx-bulk": "true"}
        validated_items = []

        for item in items:
            # Ensure all the items are valid.  They should be in the same
            # format as if a user is adding a single item.  This also handles
            # checking the blueprint for each item
            # tags should be added on a per item basis
            self._add_tags(item)
            validated_items.append(self._validate(encrypt=encrypt, **item))

        resp = self.add(
            items=validated_items,
            headers=headers,
            _is_validated=True,
            # Don't upload as we need to handle
            # the file upload manually
            upload=False,
            parent_class=ItemAddManyEntity,
            **kwargs,
        )

        # We have all the data to create the files, but the indexes have
        # been split up compared to the response.  Therefore, inject blank
        # values into the response where there are errors.  This means that
        # the structure will match the original `items` that the user specified
        # (as the API preserves order when bulk creating data)
        ERRORED_KEY = None
        for _ in resp["errors"].keys():
            resp["items"].insert(int(_), ERRORED_KEY)
        uploaded_files = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Allows for partial success (i.e. some files uploaded successfully,
            # others did not)
            for index, item in enumerate(items):
                # Iterate the original `items` provided by the user
                created_item = resp["items"][index]
                if item.get("source") and created_item is not None:
                    # There was a file on the original item and it was also
                    # successfully created by the API.  Upload the file as normal
                    uploaded_files[
                        executor.submit(
                            self._upload_file,
                            entity=resp["items"][index],
                            source=item["source"],
                        )
                    ] = index
            for future in concurrent.futures.as_completed(uploaded_files):
                # Handles updating the error response if any files failed to
                # upload
                index = uploaded_files[future]
                try:
                    future.result()
                except QalxAPIResponseError as exc:
                    # There was an error uploading this single file.  Update
                    # the response dict accordingly.
                    resp["items"].pop(index)
                    resp["items_created"] = resp["items_created"] - 1
                    resp["items_errored"] = resp["items_errored"] + 1
                    resp["errors"][index] = exc

        # Finally, remove all the `None` values from the items as these were
        # errors that we are done with
        resp["items"] = list(
            filter(lambda x: x is not ERRORED_KEY, resp["items"])
        )
        if resp["errors"]:
            for index, error in resp["errors"].items():
                self.session.log.warning(
                    f"Error bulk creating at index `{index}`. "
                    f"Error: `{error}`. "
                    f"Original Data: `{items[int(index)]}`"
                )
        return resp
