compile:
	python manage.py makemigrations books
	python manage.py makemigrations bookrequest
	python manage.py migrate			

run:
	python manage.py runserver
