# Friendly ([Live](http://ec2-13-232-26-147.ap-south-1.compute.amazonaws.com))
Welcome to the repository for our Django application, **Friendly**! This README serves as your guide on setting up the application.
We offer two setups for your convenience: the **Dockerized setup** and the **Manual setup**. The **Dockerized setup** is ideal for **deployment** purposes and running the application. The **Manual setup** is ideal for the **development environment**. Combining these setups ensures a seamless deployment and development experience. Follow the steps below to get started.

## Dockerized Setup (Preferred for deployment)

### Prerequisites
- [Docker](ec2-13-232-26-147.ap-south-1.compute.amazonaws.com)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/DubeyAkshat/friendly.git
    ```

2. Navigate to the `friendly` directory:
    ```bash
    cd friendly
    ```
    
3. Create a `.env` file in the `friendly` directory. It is advisable to refer to the `.env.example` and create the environment variables. For a quick setup, you can copy the environment variables given below:
   ```dotenv
    DEBUG=False
    SECRET_KEY=my_secret_key
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
    POSTGRES_USER=friendly
    POSTGRES_PASSWORD=friendly
    POSTGRES_HOST=postgres_db
    POSTGRES_DB=friendly
    POSTGRES_PORT=5432
    NGINX_HOST_PORT=80
   ```
    Replace the `SECRET_KEY` with a securely generated secret key for your Django application. You can use online tools or Django's `django.core.management.utils.get_random_secret_key()` method to generate a new key. Make sure to keep this key confidential and never share it publicly.
    Also, you can add your production domain or IP address to the `DJANGO_ALLOWED_HOST` if you intend to deploy the application.

4. Build the docker images and start the docker containers in daemon mode:
    ```bash
    docker-compose up --build -d
    ```
    This command will build the Docker image and start the application along with its dependencies.

5. Access the application at `http://localhost` if the `NGINX_HOST_PORT` environment variable is set to `80`. In case you've modified the `NGINX_HOST_PORT` to a different value, the application can be reached at `http://localhost:{NGINX_HOST_PORT}`, or through the configured domains in the `DJANGO_ALLOWED_HOSTS` environment variable.

6. Run migrations:
    ```bash
    docker-compose exec django_app python manage.py makemigrations
    ```
    
7. You can create a `superuser` by using the command:
    ```bash
    docker-compose exec django_app python manage.py createsuperuser
    ```
    Afterward, access the admin interface at the configured base URL, either directly (`http://localhost/admin/` or `http://localhost:{NGINX_HOST_PORT}/admin/`) or through the specified domain(s) in the `DJANGO_ALLOWED_HOSTS variable`.

8. To stop the containers and the application:
    ```bash
    docker-compose down
    ```

## Manual Setup (Preferred for development environment)
If you prefer not to use Docker, you can manually set up and run the application or use this setup as development environment using the following steps:

### Prerequisites
- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [PostgreSQL](https://www.postgresql.org/download/)

### Steps
1. Database setup: 
    - Install [PostgreSQL](https://www.postgresql.org/download/)
    - Create user, database and role for the application:
      - Open a PostgreSQL shell or use a tool like pgAdmin
      - Run the following commands to create a user, a database, and a role for your Django application. Replace `<user>`, `<password>`, `<host>`, `<port>`, and `<database>` with your preferred values:
        ```sql
        CREATE USER <user> WITH PASSWORD '<password>';
        CREATE DATABASE <database> OWNER <user>;
        ALTER ROLE <user> SET client_encoding TO 'utf8';
        ALTER ROLE <user> SET default_transaction_isolation TO 'read committed';
        ALTER ROLE <user> SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE <database> TO <user>;
        ```

2. Clone the repository:
    ```bash
    git clone https://github.com/DubeyAkshat/friendly.git
    ```

3. Navigate to the `friendly` directory:
    ```bash
    cd friendly
    ```

4. Create a virtual environment: 
    ```bash
    python -m venv venv
    ```

5. Activate the virtual environment: 
    ```bash
    source venv/bin/activate
    ```
    - On Windows: 
        ```bash
        .\venv\Scripts\Activate.ps1`
        ```

6. Create a `.env` file in the `friendly` directory. It is advisable to refer to the `.env.example` and create the environment variables. For a quick setup, you can copy the environment variables given below:
   ```dotenv
    DEBUG=True
    SECRET_KEY=my_secret_key
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
    DATABASE_URL=postgres://<user>:<password>@<host>:<port>/<database>
   ```
    Replace the `SECRET_KEY` with a securely generated secret key for your Django application. You can use online tools or Django's `django.core.management.utils.get_random_secret_key()` method to generate a new key. Make sure to keep this key confidential and never share it publicly.
    Replace `<user>`, `<password>`, `<host>`, `<port>` & `<database>` with the actual values in the `DATABASE_URL`

7. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

8. Run migrations: 
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

9. Collect static files:
    ```bash
    python manage.py collectstatic --noinput --clear
    ```

10. Run the application:
    Navigate to the `friendly/django_app/` directory:
    ```bash
    cd django_app
    ```
    Start the server:
    - With Gunicorn: 
        ```bash
        gunicorn friendly_django.wsgi:application --bind 0.0.0.0:8000 --reload
        ```
    - Without Gunicorn:
        ```bash
        python manage.py runserver
        ```
    Access the application at `http://localhost:8000` or through the configured domains in the `DJANGO_ALLOWED_HOSTS` environment variable.

11. To create a `superuser`:
    ```bash
    python manage.py createsuperuser
    ```
    Afterward, access the admin interface at the configured base URL, either directly (`http://localhost:8000/admin/`) or through the specified domain(s) in the `DJANGO_ALLOWED_HOSTS` variable.

12. To stop the Django development server, simply press `Ctrl+C` in the terminal where the server is running.