# Shooter stats
The statistics server for shooter game.
[![Build Status](https://travis-ci.org/PetrushynskyiOleksii/shooter-stats.svg?branch=master)](https://travis-ci.org/PetrushynskyiOleksii/shooter-stats)

## Requirements
- python 3.7.0
- postgreSQL

## Endpoints
| Method | URL | Description |
|--------|-----------------------------|-------------------------------------------------------------|
| GET | /servers | Return a paginated list of servers. |
| POST | /servers | Create a new server instance. |
| GET | /servers/{endpoint} | Return a single server instance by *endpoint*. |
| PATCH | /servers/{endpoint} | Update server instance with the specified *endpoint*. |
| GET | /players | Returns a paginated list of players. |
| POST | /players | Create a new player instance. |
| GET | /players/{nickname} | Return a single player instance by *nickname*. |
| GET | /servers/{endpoint}/players | Returns a list of server players. |
| POST | /matches | Create a new match instance. |
| GET | /matches/{id} | Return a single match instance by *id*. |
| GET | /servers/{endpoint}/matches | Returns a paginated list of server matches ordered by date. |
| GET | /players/{nickname}/matches | Returns a paginated list of player matches ordered by date. |

*For more detail information about endpoints you need to go through the following section and look point #9.*

## How to run it locally?
1. Clone this repository and cd into the cloned folder.
   - SSH - `$ git clonegit@github.com:PetrushynskyiOleksii/shooter-stats.git`
   - HTTPS - `$ git clone https://github.com/PetrushynskyiOleksii/shooter-stats.git`
2. Create virtual environment and activate it.
3. Create environment variables:
    ```
    export APP_SETTINGS='development'
    export DATABASE_URL='postgresql://shooter:shooter@localhost/shooterstats'
    export SECRET='secret key'
    ```
4. Create user in your postgres: `CREATE USER shooter WITH PASSWORD 'shooter';`
5. Create database in your psql console: `CREATE DATABASE shooterstats OWNER shooter;`
6. Alter privileges to user: `ALTER USER shooter CREATEDB;`
7. Run migrate from project dir: `python src/manage.py migrate && python src/manage.py upgrade`
8. Run server: `python src/run.py`
9. Read swagger documentation: `127.0.0.1:5000/ui`
