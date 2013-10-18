develop:
	python setup.py develop
	(cd demo; python setup.py develop)
	demo syncdb
