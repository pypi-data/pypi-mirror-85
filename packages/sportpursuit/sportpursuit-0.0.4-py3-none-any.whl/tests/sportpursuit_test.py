import unittest
from sportpursuit.sportpursuit import GetData
from unittest.mock import MagicMock, patch
from unittest import mock
import psycopg2


class TestGetRedshiftData(unittest.TestCase):
	def test_fetching_simple_redshift_data(self):

		# check a simple query genuinely returns results
		
		test_sql = "select * from magento_sales_flat_order limit 10;"
		function_result = GetData.get_redshift_data(test_sql)
		self.assertTrue(len(function_result) == 10)


class TestExecuteRedshiftCommand(unittest.TestCase):


	def test_executing_simple_redshift_command(self):
		# since the function in question doesn't return anything from the sql query
		# the test mocks the connection and checks the function runs end to end
		# if the function ever is extended to do some processing or manipulation this will need to be updated too

		test_sql = 'select 7'
		with mock.patch('psycopg2.connect') as mock_connect:
			result = GetData.execute_redshift_command(test_sql)
		self.assertEqual(test_sql, result)

	
class TestGetRedshiftCredentials(unittest.TestCase):
	def test_credentials_return_something(self):
		# just want to check the credentials read in is producing something

		test_redshift_username, test_redshift_password = GetData.get_redshift_credentials()

		self.assertTrue(len(test_redshift_username) > 0)
		self.assertTrue(len(test_redshift_password) > 0)

