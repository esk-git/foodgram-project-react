# Foodgram
«Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.  Проект состоит из бэкенд-приложения на Django и фронтенд-приложения на React.
### Немного о технологиях
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
#### Проект доступен по [адресу](https://foodgram.servehalflife.com/)
```
https://foodgram.servehalflife.com/
```
### Установка и запуск
- Клонировать репозиторий
```
https://github.com/esk-git/foodgram-project-react.git
```
- Скопировать на сервер файлы docker-compose.production.yml, nginx.conf из папки infra
```
scp docker-compose.yml nginx.conf username@IP:/home/username/   # username - имя пользователя на сервере
                                                                # IP - публичный IP сервера
```
- Запустить контейнеры
```
docker-compose -f docker-compose.production.yml up -d --build
```
- После успешного запуска контейнеров необходимо создать суперпользователя:
```
sudo docker exec -it foodgram_backend bash
```
```
python manage.py createsuperuser
```
Когда суперпользователь будет создан, для загрузки ингредиентов необходимо войти в админку -> Ингредиенты и осуществить импорт файла ingredients.json из каталога data/ingredients.json.
#### Backend автор
Каликов Евгений