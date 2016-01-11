run: clean
	. venv/bin/activate && foreman run python2 run.py

clean:
	find . -name '*.pyc' -delete

# Upgrade the db to a new schema
upgrade:
	psql -d hmint -c 'drop schema public cascade; create schema public;'
	foreman run python2 manage.py db upgrade

# Generate a migration for the current schema
migrate:
	psql -d hmint -c 'drop schema public cascade; create schema public;'
	foreman run python2 manage.py db migrate

# db_dump:
# 	pg_dump --data-only hmint > local.db

# db_restore: local.db
# 	psql hmint < local.db
