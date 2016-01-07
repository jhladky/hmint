run: clean
	. venv/bin/activate && foreman run python2 run.py

clean:
	find . -name '*.pyc' -delete
