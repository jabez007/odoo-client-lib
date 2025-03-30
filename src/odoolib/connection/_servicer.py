import logging
from typing import Optional

from ..connector._connector import Connector
from ..service import Service
from .authentication_error import AuthenticationError


class Servicer(object):

    def __init__(
        self,
        connector: Connector,
        database: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        user_id: Optional[int] = None,
    ):
        self._logger = logging.getLogger(
            f"{str.join('.', __name__.split('.')[:-1])}.{connector.PROTOCOL}"
        )
        self.connector = connector
        self.set_login_info(database, login, password, user_id)

    def set_login_info(
        self,
        database: Optional[str],
        login: Optional[str],
        password: Optional[str],
        user_id: Optional[int] = None,
    ):
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

    def get_service(self, service_name: str) -> Service:
        """
        Returns a Service instance to allow easy manipulation of one of the services offered by the remote server.
        Please note this Connection instance does not need to have valid authentication information since authentication
        is only necessary for the "object" service that handles models.

        :param service_name: The name of the service.
        """
        return self.connector.get_service(service_name)
