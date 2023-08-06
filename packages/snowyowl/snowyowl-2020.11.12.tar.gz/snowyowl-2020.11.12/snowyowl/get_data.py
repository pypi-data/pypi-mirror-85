from snowflake.connector import connect, connection
from pandas import DataFrame


def get_data(query, user=None, password=None, account=None, warehouse=None, connection=None, database='analytics',):
	"""
	:type query: str
	:type user: str
	:type password: str
	:type account: str
	:type warehouse: str
	:type connection: connection
	:rtype: DataFrame
	"""
	print(query)
	if connection is None:
		if user is None or password is None or account is None:
			raise ValueError('user, password, and account should be provided for new connection!')
		connection = connect(user=user, password=password, account=account)
		connection_is_temporary = True
	else:
		connection_is_temporary = False

	try:
		connection.cursor().execute(f"use warehouse {warehouse}")
		connection.cursor().execute(f"use database {database}")

		cur = connection.cursor().execute(query)
		df = DataFrame.from_records(iter(cur), columns=[x[0] for x in cur.description])
		df.columns = [x.lower() for x in df.columns]
		return df
	finally:
		connection.cursor().close()
		if connection_is_temporary:
			connection.close()
