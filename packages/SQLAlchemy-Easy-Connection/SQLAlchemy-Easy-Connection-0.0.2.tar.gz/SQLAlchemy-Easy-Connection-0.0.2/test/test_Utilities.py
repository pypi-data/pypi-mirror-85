import unittest
from SQLAlchemyEasyConnection import Utilities


class TestUtilities(unittest.TestCase):
    def test_generate_connection_string(self):
        # Create a Single string
        # Expected test
        expected_string = Utilities.generate_connection_string(type_database="postgresql", user="foo", password="bar",
                                                               database="mydatabase")
        self.assertEqual(expected_string, "postgresql://foo:bar@localhost/mydatabase")  # pass

        # Attempting to crack code
        connection_string = Utilities.generate_connection_string()
        self.assertEqual(connection_string, "://localhost/")  # pass

        # if using sqlite file, this be a special case in.
        # Expected test to use SQLite
        connection_sqlite_string2 = Utilities.generate_connection_string(type_database="sqlite",
                                                                         database="path_to_local/database.db")
        self.assertEqual(connection_sqlite_string2, "sqlite:///path_to_local/database.db")  # pass

        # Attempting to crack code
        # if only set type_database equal sqlite, the default host "localhost" will don't exist
        connection_sqlite_string = Utilities.generate_connection_string(type_database="sqlite")
        self.assertEqual(connection_sqlite_string, "sqlite:///")  # pass


if __name__ == '__main__':
    unittest.main()
