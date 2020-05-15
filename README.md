# iCrawler

Basic setup to run ScrapyD + Django and save it in Django Models. You can be up and running in just a few minutes. This template includes

- Basic structure of a Django project.
- Basic structure for scrapy.
- Configuration of scrapy in order to access Django models objects.
- Basic scrapy pipeline to save crawled objets to Django models.
- Basic spider definition
- Basic demo from the oficial tutorial that crawls data from http://quotes.toscrape.com

## Setup

1. Install requirements

    This will make pip install dependencies for `iCrawler`.

    ```bash
    pip install -r requirements.txt
    ```

2. Migrations

    Make sure database is configured properly if you are not using `docker-compose` in this project. From root directory run migrations for django-models

    ```bash
    python manage.py migrate
    ```

# Start the project

There are 2 options to run this project, run this project manually into your machine or using docker by docker-compose.

### Manual

In order to start this project you will need to have running Django and Scrapyd at the same time.

1. Running django (iCrawler)

    ```bash
    python manager.py runserver
    ```

2. Run scrapyd.

    Find more command in [Scrapy documentation](https://docs.scrapy.org/en/latest/index.html)

    ```bash
    $ cd scrapy_app
    $ scrapyd
    ```

### Docker way

If you don't have docker installed in your machine go to [Docker Site to get docker and install it](https://docs.docker.com/get-docker/). Assume you have `docker-compose` installed.

```bash
docker-compose up --build --abort-on-container-exit
```

Run migrations, this will run migrations and will migrate django models into database, check docker-compose.yaml file block service db. All models and data will be stored in that service db.

```bash
docker-compose exec app sh -c "python manage.py migrate && python manage.py createsuperuser"
```

If all goes well, django icrawler will be running on `http://localhost:8080` and scrapy on `http://localhost:6800`, and you can access database using your postgresql client with this database credentials [host: localhost, user: postgres, dbname: icrawler, password see in docker-compose.yaml file]

This repo is inspired by an article from [Ali Oğuzhan Yıldız available in medium.com](https://medium.com/@ali_oguzhan/how-to-use-scrapy-with-django-application-c16fabd0e62e)
