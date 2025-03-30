import unittest

import odoolib


class TestAsyncSequenceFunctions(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        pass

    def _conn(self, protocol):
        return odoolib.get_connection(
            hostname="localhost",
            protocol=protocol,
            database="test",
            login="admin",
            password="a",
        )

    def _get_protocols(self):
        """Returns available protocols."""
        return ["xmlrpc", "jsonrpc"]

    async def test_simple_async(self):
        """Tests async read."""
        for protocol in self._get_protocols():
            connection = self._conn(protocol)

            res = await connection.get_model("res.users").read.async_(1)

            self.assertEqual(res["id"], 1)

    async def test_user_context_async(self):
        """Tests async user context retrieval."""
        for protocol in self._get_protocols():
            connection = self._conn(protocol)

            await connection.async_get_user_context()

    async def test_search_count_async(self):
        """Tests async search and count."""
        for protocol in self._get_protocols():
            connection = self._conn(protocol)
            country_model = connection.get_model("res.country")

            de_country_ids = await country_model.search.async_(
                [("name", "ilike", "de")]
            )
            de_country_count = await country_model.search_count.async_(
                [("name", "ilike", "de")]
            )

            self.assertEqual(de_country_count, len(de_country_ids))


if __name__ == "__main__":
    unittest.main()
