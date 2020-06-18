worker:
	celery -A tasks worker --loglevel=info

beat:
	celery -A tasks beat --loglevel=info