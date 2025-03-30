import logging

from .connection._servicer import Servicer


class Model(object):
    """
    Useful class to dialog with one of the models provided by an Odoo server.
    An instance of this class depends on a Connection instance with valid authentication information.
    """

    def __init__(self, connection: Servicer, model_name: str):
        """
        :param connection: A valid Connection instance with correct authentication information.
        :param model_name: The name of the model.
        """
        self.connection = connection
        self.model_name = model_name
        self._logger = logging.getLogger(f"{__name__}.{model_name}")

    def __getattr__(self, method):
        """
        Provides proxy methods that will forward calls to the model on the remote Odoo server.

        :param method: The method for the linked model (search, read, write, unlink, create, ...)
        """

        def proxy(*args, **kw):
            """
            :param args: A list of values for the method
            """
            self.connection.check_login(False)
            self._logger.debug("args (sync): %r", args)
            result = self.connection.get_service("object").execute_kw(
                self.connection.database,
                self.connection.user_id,
                self.connection.password,
                self.model_name,
                method,
                args,
                kw,
            )
            return self._process_result(method, args, result)

        async def async_proxy(*args, **kw):
            """
            :param args: A list of values for the method
            """
            await self.connection.async_check_login(False)
            self._logger.debug("args (async): %r", args)
            result = await self.connection.get_service("object").execute_kw.async_(
                self.connection.database,
                self.connection.user_id,
                self.connection.password,
                self.model_name,
                method,
                args,
                kw,
            )
            return self._process_result(method, args, result)

        # Attach `.async_` to the sync proxy for async usage
        proxy.async_ = async_proxy
        return proxy

    def _process_result(self, method, args, result):
        """
        Handles post-processing for 'read' operations.
        """
        if method == "read":
            if isinstance(result, list) and len(result) > 0 and "id" in result[0]:
                index = {}
                for r in result:
                    index[r["id"]] = r
                if isinstance(args[0], list):
                    result = [index[x] for x in args[0] if x in index]
                elif args[0] in index:
                    result = index[args[0]]
                else:
                    result = False
        self._logger.debug("result: %r", result)
        return result

    def search_read(
        self, domain=None, fields=None, offset=0, limit=None, order=None, context=None
    ):
        """
        A shortcut method to combine a search() and a read().

        :param domain: The domain for the search.
        :param fields: The fields to extract (can be None or [] to extract all fields).
        :param offset: The offset for the rows to read.
        :param limit: The maximum number of rows to read.
        :param order: The order to class the rows.
        :param context: The context.
        :return: A list of dictionaries containing all the specified fields.
        """
        record_ids = self.search(
            domain or [], offset, limit or False, order or False, context=context or {}
        )
        if not record_ids:
            return []
        records = self.read(record_ids, fields or [], context=context or {})
        return records

    async def async_search_read(
        self, domain=None, fields=None, offset=0, limit=None, order=None, context=None
    ):
        """
        A shortcut method to combine a search() and a read().

        :param domain: The domain for the search.
        :param fields: The fields to extract (can be None or [] to extract all fields).
        :param offset: The offset for the rows to read.
        :param limit: The maximum number of rows to read.
        :param order: The order to class the rows.
        :param context: The context.
        :return: A list of dictionaries containing all the specified fields.
        """
        record_ids = await self.search.async_(
            domain or [], offset, limit or False, order or False, context=context or {}
        )
        if not record_ids:
            return []
        records = await self.read.async_(
            record_ids, fields or [], context=context or {}
        )
        return records
