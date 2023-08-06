from snowflake.connector import connect, connection


def run_query(
		query,
		user=None, password=None, account=None, warehouse=None, connection=None,
		database='analytics'
):
	"""
	:type query: str
	:type user: str
	:type password: str
	:type account: str
	:type warehouse: str
	:type connection: connection
	"""

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
		connection.cursor().execute(query)

	finally:
		connection.cursor().close()
		if connection_is_temporary:
			connection.close()
