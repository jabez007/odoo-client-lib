import logging

from .connector._connector import Connector
from .model import Model


class AuthenticationError(Exception):
    """
    An error thrown when an authentication to an Odoo server failed.
    """

    pass


class Connection(object):
    """
    A class to represent a connection with authentication to an Odoo Server.
    It also provides utility methods to interact with the server more easily.
    """

    def __init__(
        self,
        connector: Connector,
        database=None,
        login=None,
        password=None,
        user_id=None,
    ):
        """
        Initialize with login information. The login information is facultative to allow specifying
        it after the initialization of this object.

        :param connector: A valid Connector instance to send messages to the remote server.
        :param database: The name of the database to work on.
        :param login: The login of the user.
        :param password: The password of the user.
        :param user_id: The user id is a number identifying the user. This is only useful if you
        already know it, in most cases you don't need to specify it.
        """
        self.connector = connector
        self._logger = logging.getLogger(f"{__name__}.{connector.PROTOCOL}")
        self.set_login_info(database, login, password, user_id)
        self.user_context = None

    def set_login_info(self, database, login, password, user_id=None):
        """
        Set login information after the initialisation of this object.

        :param connector: A valid Connector instance to send messages to the remote server.
        :param database: The name of the database to work on.
        :param login: The login of the user.
        :param password: The password of the user.
        :param user_id: The user id is a number identifying the user. This is only useful if you
        already know it, in most cases you don't need to specify it.
        """
        self.database, self.login, self.password = database, login, password

        self.user_id = user_id

    def check_login(self, force=True):
        """
        Checks that the login information is valid. Throws an AuthenticationError if the
        authentication fails.

        :param force: Force to re-check even if this Connection was already validated previously.
        Default to True.
        """
        if self.user_id and not force:
            return

        if not self.database or not self.login or self.password is None:
            raise AuthenticationError("Credentials not provided")

        # TODO use authenticate instead of login
        self.user_id = self.get_service("common").login(
            self.database, self.login, self.password
        )
        if not self.user_id:
            raise AuthenticationError("Authentication failure")
        self._logger.debug("Authenticated with user id %s", self.user_id)

    def get_user_context(self):
        """
        Query the default context of the user.
        """
        if not self.user_context:
            self.user_context = self.get_model("res.users").context_get()
        return self.user_context

    def get_model(self, model_name):
        """
        Returns a Model instance to allow easy remote manipulation of an Odoo model.

        :param model_name: The name of the model.
        """
        return Model(self, model_name)

    def get_service(self, service_name):
        """
        Returns a Service instance to allow easy manipulation of one of the services offered by the remote server.
        Please note this Connection instance does not need to have valid authentication information since authentication
        is only necessary for the "object" service that handles models.

        :param service_name: The name of the service.
        """
        return self.connector.get_service(service_name)
