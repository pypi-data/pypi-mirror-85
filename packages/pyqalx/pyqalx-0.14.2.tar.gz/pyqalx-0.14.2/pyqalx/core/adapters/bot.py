from pyqalx.core.adapters.adapter import (
    QalxNamedEntityAdapter,
    QalxUpdateStatusAdapter,
)
from pyqalx.core.entities import Bot


class QalxBot(QalxNamedEntityAdapter, QalxUpdateStatusAdapter):
    _entity_class = Bot
    _user_only_methods = ["add"]
    _bot_only_methods = ["replace_workers"]

    def add(self, name, config, meta=None, **kwargs):
        """
        Creates a `Bot` instance.

        :param name: The name that this bot will be given
        :type name: str
        :param config: The bots config
        :type config: dict
        :param meta: A dictionary of metadata to store
        :type meta: dict
        :return: The newly created `Bot` instance
        """
        return super(QalxBot, self).add(
            host=self.session._host_info,
            name=name,
            meta=meta,
            config=config,
            **kwargs,
        )

    def replace_workers(self, bot_entity, workers):
        """
        Completely replaces any Workers on the given bot.  Will return the
        replaced workers in an unpacked state

        :param bot_entity: The ~entities.bot.Bot entity that is being changed
        :param workers: The number of workers that this bot should have
        :return: A ~entities.bot.Bot instance with the updated workers
        """
        guid = bot_entity["guid"]
        detail_endpoint = self.detail_endpoint(guid=guid)
        endpoint = f"{detail_endpoint}/replace-workers"
        self.session.log.debug(
            f"replace workers {self.entity_class.entity_type} with"
            f" guid {guid} with {endpoint}"
        )

        resp = self._process_api_request("patch", endpoint, workers=workers)
        return self._process_api_response(resp)

    def _signal_workers(self, entity, signal_method, *args, **kwargs):
        """
        Helper method for calling signals on workers.  A bot doesn't have
        the concept of `signals`.  Instead, we call a signal method we just
        apply this to all the workers on the bot
        """

        for worker in entity.get("workers", []):
            worker_method = getattr(self.session.worker, signal_method)
            worker_method(worker, bot_entity=entity, *args, **kwargs)

    def stop(self, entity, **kwargs):
        """
        Stops all the workers on the bot
        """
        self._signal_workers(entity, signal_method="stop", **kwargs)

    def resume(self, entity, **kwargs):
        """
        Resumes all the workers on the bot
        """
        self._signal_workers(entity, signal_method="resume", **kwargs)

    def terminate(self, entity, *args, **kwargs):
        """
        Terminates all the workers on the bot
        """
        self._signal_workers(entity, signal_method="terminate", *args, **kwargs)
