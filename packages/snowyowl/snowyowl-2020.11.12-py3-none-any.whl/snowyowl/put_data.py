from snowflake.connector import connect, connection
from sqlalchemy import create_engine, event
from pandas import DataFrame


def put_data(
		data, schema, table,
		user=None, password=None, account=None, warehouse=None, connection=None,
		database='analytics'
):
	"""
	:type data: DataFrame
	:type schema: str
	:type table: str
	:type user: str
	:type password: str
	:type account: str
	:type warehouse: str
	:type connection: connection
	"""
	table = table.upper()
	schema = schema.upper()

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

		cur = connection.cursor()
		try:
			cur.execute(f'create schema {schema}')
		except:
			pass


		engine = create_engine(
			f'snowflake://{user}:{password}@{account}/{database}/{schema}?role=SYSADMIN&warehouse={warehouse}'
		)

		@event.listens_for(engine, 'before_cursor_execute')
		def receive_before_cursor_execute(connection, cursor, statement, params, context, executemany):
			if executemany:
				cursor.fast_executemany = True
				cursor.commit()
		data.to_sql(table, con=engine, index=False, if_exists='replace', chunksize=None)
	finally:
		connection.cursor().close()
		if connection_is_temporary:
			connection.close()
