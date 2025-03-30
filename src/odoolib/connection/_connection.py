from typing import Optional

from ..connector._connector import Connector
from ..model import Model
from ._servicer import Servicer


class Connection(Servicer):
    """
    A class to represent a connection with authentication to an Odoo Server.
    It also provides utility methods to interact with the server more easily.
    """

    def __init__(
        self,
        connector: Connector,
        database: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        user_id: Optional[int] = None,
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
        super(Connection, self).__init__(connector, database, login, password, user_id)
        self.user_context = None

    def get_user_context(self):
        """
        Query the default context of the user.
        """
        if not self.user_context:
            self.user_context = self.get_model("res.users").context_get()
        return self.user_context

    def get_model(self, model_name: str) -> Model:
        """
        Returns a Model instance to allow easy remote manipulation of an Odoo model.

        :param model_name: The name of the model.
        """
        return Model(self, model_name)
