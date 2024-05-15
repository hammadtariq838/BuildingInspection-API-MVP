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

## Django commands
1. First Time Setup
```bash
  virtualenv venv
  pip install -r requirements.txt
  python manage.py migrate
```
2. Create Super User
```bash
  python manage.py createsuperuser
```
3. Running the server
```bash
  python manage.py runserver
```
4. Check & Create Migrations
```bash
  python manage.py makemigrations
  python manage.py migrate
```




## API Endpoints

Flow:
  Create a project -> Select Template -> Upload Assets -> Run Analysis -> View Results
  


Project Types:
 - Crack Detection
 - Moss Detection
 - Before After