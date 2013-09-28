MANAGE=python egonomist/manage.py

run:
	$(MANAGE) runserver

syncdb:
	$(MANAGE) syncdb --noinput

shell:
	$(MANAGE) shell