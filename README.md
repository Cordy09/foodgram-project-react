# Проект Foodgram «Продуктовый помощник»

## Описание

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


## Как запустить проект

#### Клонировать репозиторий и перейти в него в командной строке

```shell
git clone https://github.com/Cordy09/foodgram-project-react.git
cd foodgram-project-react/backend
```


#### Запустить проект

```shell
cd ../infra
docker-compose up -d --build
```

#### Подготовить базу данных и статику 

```shell
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend python manage.py csv
```

## Проект доступен по следующим ссылкам:

* http://foodgram-project.ddnsking.com - главная страница


* http://foodgram-project.ddnsking.com/admin/ - админ-панель


* http://foodgram-project.ddnsking.com/api/docs/ - redoc.html


Автор бэкенда: Коваленко Анна

![example workflow](https://github.com/Cordy09foodgram-project-react/actions/workflows/workflow.yml/badge.svg)