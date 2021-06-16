# wc-guide-backend
![Overview](doc/images/wc_guide_overview.png)
## Development
### Prerequisites
To start development make sure the following applications are installed:
 - Docker (https://docs.docker.com/get-docker/)
 - Poetry (https://python-poetry.org/docs/)
 - GDAL (https://gdal.org/)
### Setup

#### Database
Run PostgreSQL Database with PostGIS extension.
```sh
docker run --name wc-guide-backend-db -e POSTGRES_DB=wc-guide-backend-db -e POSTGRES_USER=guide -e POSTGRES_PASSWORD=wc-guide-backend -d -p 5432:5432 mdillon/postgis
```
#### Backend
Run Django Backend.
```sh
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```
Now you can navigate to http://localhost:8000/swagger/ to get the API documentation.

#### Testing
To run the test locally execute the following command:
```sh
 poetry run pytest -v -s
```
Further, there is a GitHub Action that executes the tests on over push to main and pull request.
[GitHub Action Testing](.github/workflow/testing.yml)


#### Examples
If you want to query all toilets within a certain bounding box, you can do the following request:
```sh
curl get http://localhost:8000/toilets/?in_bbox=9.283283,47.081593,9.372739,47.133249
```