MANAGE=python egonomist/manage.py

run:
	$(MANAGE) runserver 0.0.0.0:8000

syncdb:
	$(MANAGE) syncdb --noinput

shell:
	$(MANAGE) shell

celery_worker:
	$(MANAGE) celery worker -c 1 -l DEBUG --purge

migrate:
	$(MANAGE) migrate
