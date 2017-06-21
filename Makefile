VIRTUALENV = virtualenv
TEMPDIR := $(shell mktemp -d)

develop:
	python setup.py develop

demo:
	python setup.py develop
	(cd demo; python setup.py develop)
	demo migrate
	demo runserver

build-requirements:
	$(VIRTUALENV) $(TEMPDIR)
	$(TEMPDIR)/bin/pip install -U pip
	$(TEMPDIR)/bin/pip install -Ue "."
	$(TEMPDIR)/bin/pip freeze | grep -v -- '-e' > requirements-release.txt
