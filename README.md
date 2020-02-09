# Validus - Capital Call

Validus Fund V is a Private Equity Fund and invests in several kinds of Assets in North America. The fund managers need a system to determine which investor(s) they need to call in order to invest in a new investment. The methodology they implement is ‘First In, First Out (FIFO)’

## Installation - Dev

Instructions to clone and run the project from your local machine.

```
	git clone git@github.com:stephenmullens/validus.git
	cd validus
	pipenv install
	pipenv shell
	cd capital_call
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver
```
Open your web browser to:
http://127.0.0.1:8000/

## Misc
- Sample data is loaded with the database migrations.
- Data is stored in SQLite for simplicity.
- The "Reset Data" button clears the database and reloads the sample data


## Code Styling:
- Python should follow the PEP8 standard.
- HTML should follow the HTML5 standard and pass W3C validation.


## Testing Policy:

### Continuous Validation:
- All user inputs (POST / GET) should be validated for completeness, datatype and permitted values (eg no negative amounts).
- All user inputs (POST) should be evaluated and cleaned for SQL / JS Injection.
- All changes to the database should be vetted such that the changes follow all necessary matching rules.
- All changes to the database should perform the following:

a) @transaction.atomic to ensure only complete execution is captured.

b) Each fund should be checked to ensure that more funds have not been allocated to it, than were committed.

c) The difference between the total allocated funds before and after the call request match the call request size. On very large datasets this may become a challenge, and should be assessed.

d) The database should be locked during any mutations to the database to prevent two or more call requests being added at the same time and interacting. Alternatively move all mutations async into a queuing system with Celery or otherwise with a single thread.


### Unit Testing:
1) Validate database can be accessed and written to.
2) Load the fixtures data into the test database, verify data has loaded.
3) Create multiple test cases to capture potential edge cases. After each test is complete, clear the test database and reload the fixture:

a) Enter three new calls that will all be allocated by the first funding commitment. Verify correct allocation.

b) Enter three new calls that will consume the entire of the first and partially the second funding commitment. Verify correct allocation.

c) Create sufficient calls to consume all committed funds. No call should exactly match against an entire fund. Verify correct allocation.

d) Create sufficient calls to consume all committed funds. Exactly one call should match each commitment in the correct order. Verify correct allocation.

e) Create three calls which will consume 1cent more money than committed. Check for error, and evaluate database condition.

f) Create calls with incorrect values, such as negative numbers and confirm errors. Evaluate database condition.
