### Django reservation application install
- `git clone https://github.com/boriskrutskih/django-reservation.git`
- `cd django-reservation`

   Настройка .env окружения, пример  `.env.example`
-  Install pipenv `pip install pipenv`
- `pipenv shell`
- `pipenv install`
- `python manage.py makemigrations && python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`


### Запуск Redis для celery
- `docker run -d -p 6379:6379 redis`
- `docker container ls`


### Запуск Celery
- `celery -A reservation worker --pool=solo -l info`
