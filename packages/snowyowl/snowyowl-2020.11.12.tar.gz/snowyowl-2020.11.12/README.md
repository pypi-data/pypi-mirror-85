# *SnowyOwl*

## Usage

```python
from snowyowl import Snowflake
snowflake = Snowflake(
	user='user', 
	password='password', 
	warehouse='warehouse',
	account='account'
)

snowflake.get_data('SELECT * FROM database.schema.table LIMIT 10')
```