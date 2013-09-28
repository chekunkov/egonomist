MANAGE=python egonomist/manage.py

run:
	$(MANAGE) runserver

syncdb:
	$(MANAGE) syncdb --noinput

shell:
	$(MANAGE) shell

celery_worker:
	$(MANAGE) celery worker -c 1 -l DEBUG --purge
