FROM python:3.9

RUN apt-get update
RUN apt-get install gdal-bin -y
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /usr/src/app
COPY . .

RUN cd /usr/src/app \
    && poetry install \
    && poetry run python manage.py makemigrations \
    && poetry run python manage.py migrate

EXPOSE 80
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:80"]