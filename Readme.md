# MyMusicApp - Web Application

## Overview
MyMusicApp is a web application built with Django and MySQL, containerized using Docker and managed via `docker-compose`.

## Prerequisites
Before running the application, ensure you have the following installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python (if running locally outside of Docker)

## Project Setup & Running the Application

### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/mymusicapp.git
cd mymusicapp
```

### 2. Start the Application Using Docker Compose
```sh
docker-compose up -d
```
This command will:
- Pull necessary images and build the web container (`mymusicapp-web`)
- Start the MySQL database container (`mymusicapp-db`)
- Run the Django application

### 3. Check Running Containers
```sh
docker ps
```
Expected output:
```sh
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                               NAMES
ef3d59a0a0d6   mymusicapp-web:latest   "gunicorn --bind 0.0…"   X minutes ago   Up X minutes   0.0.0.0:8000->8000/tcp              mymusicapp-web-1
b96d9b60fb3a   mysql:latest            "docker-entrypoint.s…"   X minutes ago   Up X minutes   33060/tcp, 0.0.0.0:3307->3306/tcp   mymusicapp-db-1
```

### 4. Fixing Database Issues (If Needed)
If you encounter an error such as:
```sh
ProgrammingError at /
(1146, "Table 'myappdb.django_session' doesn't exist")
```
Run the following migration commands inside the `web` container:
```sh
docker-compose exec web python manage.py migrate
```

### 5. Updating `settings.py` for MySQL Port Change
Since MySQL is running on **port 3307** instead of 3306, update your `settings.py` file:

After making these changes, restart the web container:
```sh
docker-compose restart web
```
Then, apply migrations again:
```sh
docker-compose exec web python manage.py migrate
```

### 6. Accessing the Application
Once the containers are up and running, open your browser and visit:
```
http://127.0.0.1:8000/
```

## Stopping and Removing Containers
If you need to stop the application:
```sh
docker-compose down
```
This will remove the containers but keep the database volume intact.

## Additional Commands
### Viewing Logs
```sh
docker-compose logs -f
```

### Restarting Services
```sh
docker-compose restart
```

## Troubleshooting
### Issue: "Ports are not available" error
If you encounter:
```sh
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:3306 -> 0.0.0.0:0: listen tcp 0.0.0.0:3306: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
```
Solution:
- Ensure no other MySQL instance is running on your machine (`port 3306`).
- Modify `docker-compose.yml` to use a different port (e.g., `3307`).
- Restart your containers using:
  ```sh
  docker-compose down
  docker-compose up -d
  ```

### Issue: "django_session" table doesn't exist
Run migrations:
```sh
docker-compose exec web python manage.py migrate
```

## Conclusion
Your Django + MySQL app is now containerized and running via Docker Compose. Happy coding! 🎵🚀

