# wc-guide-backend

## Development

### Database
```sh
docker run --name wc-guide-backend-db -e POSTGRES_DB=wc-guide-backend-db -e POSTGRES_USER=guide -e POSTGRES_PASSWORD=wc-guide-backend -d -p 5432:5432 mdillon/postgis
```
