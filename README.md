Avito API
=


**В данной работе представлены вьюшки для:**
* Модели категорий ('/categories/')
* Модели локаций ('/locations/')
* Модели пользователей ('/users/')
* Модели объявлений ('/ads/')
* Модели подборок ('/selections/')

**В приложении используются:**
* Django ORM
* Serializers
* GenericViewSet
* ModelViewSet
* SimpleJWT

Запуск проекта:
-
1) Для того, чтобы запустить проект, скопируйте этот репозиторий на локальную машину:  
`git clone https://github.com/bchkrvn/Avito_API.git`
2) Перейдите в папку **postgres** и выполните команду:  
`docker-compose up -d`
3) После этого вернитесь в корневую папку и выполните команды:  
`python3 manage.py migrate`  
`python3 manage.py loaddata authentication/fixtures/location.json`  
`python3 manage.py loaddata ads/fixtures/category.json`  
`python3 manage.py loaddata authentication/fixtures/user.json`  
`python3 manage.py loaddata ads/fixtures/ad.json`
4) Для запуска сервера выполните команду:  
`python3 manage.py runserver`
