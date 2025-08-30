# Strava Viewer

A 3d web viewing interface of Strava activities

## How to install :

### JavaScript :
1. Run ```npm install```

### Python :
1. Navigate to folder ```strava_viewer/src/python/```
2. Run ```py -m venv venv``` to create the virtual environment
3. Run ```venv\Scripts\activate``` to activate the virtual environment
4. Run ```pip install .``` to install the packages

### PostreSQL
1. Install [Postgres](https://www.postgresql.org/download/)

## How to run :

### .env
1. Create a .env file in ```strava_viewer/src/python/```
2. Add values for _CLIENT_SECRET_ & _POSTGRES_PASSWORD_

### JavaScript :
1. Run ```npm run dev```

### Python :
1. Navigate to folder strava_viewer/src/python
2. Make sure the virtual environment is running
3. Run ```py flask_app.py```

### Postgres
1. Make sure the server is running