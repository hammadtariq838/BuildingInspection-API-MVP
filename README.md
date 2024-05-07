# Building Inspection

## Commands - Docker
1. Build the images
```bash
docker-compose build
```
2. Run the containers
```bash
docker-compose up
```
3. Build the images and run the containers
```bash
docker-compose up --build
```
4. Stop the containers
```bash
docker-compose down
```
5. Run commands inside the container
```bash
docker-compose run django python manage.py createsuperuser
```