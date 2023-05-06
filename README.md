Домашняя работа №28
=
Бочкарев Никита, Python 15
-

В данной работе представлены вьюшки для:
* Получения всех категорий (cat/ GET)
* Получения всех объявлений (ads/ GET)
* Создания новой категории (cat/ POST)
* Создания нового объявления (ads/ POST)
* Получения детальной информации о категории (cat/<id> GET)
* Получения детальной информации об объявлении (ads/<id> GET)

Запуск проекта:
-
1) Для того, чтобы запустить проект, скопируйте этот репозиторий на локальную машину:  
`git clone https://github.com/bchkrvn/HW_28.git`
2) Перейдите в каталог **postgres** и выполните команду:  
`docker-compose up -d`
3) После этого вернитесь в каталог **HW_28** и выполните команды:  
`python3 manage.py migrate`  
`python3 manage.py loaddata location.json`  
`python3 manage.py loaddata category.json`  
`python3 manage.py loaddata user.json`  
`python3 manage.py loaddata ad.json`
4) Для запуска сервера выполните команду:  
`python3 manage.py runserver`
