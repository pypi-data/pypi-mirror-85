from .get_data import get_data
from .put_data import put_data
from .run_query import run_query
import snowflake.connector # snowflake is the same as snowflake-connector-python
from snowflake.connector import SnowflakeConnection
import atexit


class Snowflake:
	def __init__(self, user, password, account, warehouse=None, database='analytics'):
		self._connection = None
		self._warehouse = None
		self._database = database
		self.connect(user=user, password=password, account=account, warehouse=warehouse)
		atexit.register(self.connection.close)

	@property
	def connection(self):
		"""
		:rtype: SnowflakeConnection
		"""
		return self._connection

	def connect(self, user, password, account, warehouse=None):
		if self._connection is not None:
			self.connection.close()
		self._connection = snowflake.connector.connect(user=user, password=password, account=account)
		self._warehouse = warehouse or self._warehouse

	def close_connection(self):
		self.connection.close()

	def __del__(self):
		self.connection.close()

	def get_data(self=None, query=None, connection=None, warehouse=None, account=None, user=None, password=None, database=None):
		if query is None:
			raise ValueError('query should be provided!')

		if self is not None:
			warehouse = warehouse or self._warehouse
			connection = connection or self._connection
			database = database or self._database

		if user is not None and password is not None and account is not None:
			connection = None

		return get_data(
			query=query, warehouse=warehouse, connection=connection, password=password, account=account,
			database=database, user=user
		)

	def put_data(self=None, data=None, schema=None, table=None, connection=None, warehouse=None, account=None, user=None, password=None, database=None):
		if self is not None:
			warehouse = warehouse or self._warehouse
			connection = connection or self._connection
			database = database or self._database

		if user is not None and password is not None and account is not None:
			connection = None

		if data is None or schema is None or table is None:
			raise TypeError('data, schema, or table is missing!')
		put_data(
			data=data, schema=schema, table=table, warehouse=warehouse, user=user,
			connection=connection, password=password, account=account, database=database,
		)

	def run_query(self=None, query=None, connection=None, warehouse=None, account=None, user=None, password=None, database=None):
		if self is not None:
			warehouse = warehouse or self._warehouse
			connection = connection or self._connection
			database = database or self._database

		if user is not None and password is not None and account is not None:
			connection = None

		if query is None:
			raise TypeError('query is missing!')
		run_query(
			query=query, warehouse=warehouse, user=user,
			connection=connection, password=password, account=account, database=database
		)
