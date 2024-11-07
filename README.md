**Project Overview:**

This project involves a Fintech web application that handles:

User Accounts (including registration and login with JWT authentication)

Transactions (deposit, withdrawal, transfer)
Background Tasks (using Celery for verifying transaction limits, sending emails, etc.)
Role-based Access Control (restricting access to certain endpoints based on user roles like admin or user)
Containerization using Docker and Docker Compose to orchestrate the services (Django app, PostgreSQL, Redis).

**Setup Steps**

**Clone the Repository:

Clone the repository and navigate to the project directory:
git clone <repository_url>
cd fintech_project

**Create Django Models**

User Model: Customize the Django User model by adding roles Admin and User.

Account Model: Implement an Account model with fields like user with a OneToOne relationship to the User Model,  account_number, bank_name, balnce

Transaction Model: Implement a Transaction model with fields like recipient_acount, with a ForeignKey relationship to the Account Model,
amount, transaction_type (deposit/withdrawal/transfer), status (e.g., pending, completed, failed), and foreign keys to the User model.

**Create Serializers**

User Serializer: Create a serializer for handling user data (registration, login).

Transaction Serializer: Handle transaction data with a serializer that ensures correct input and response formatting.

**Create Views for Registration, Transactions with necessary permisssions:**

Registration Endpoint: A POST endpoint that allows users to register with their details, which will return a JWT token upon success.

Login Endpoint: A POST endpoint that allows users to authenticate and get a JWT token for subsequent requests.

**Transaction Endpoints:**

A POST endpoint for initiating transactions (deposit, withdrawal, transfer).
A GET endpoint to view transactions for the authenticated user.
An Admin GET endpoint to view all transactions.

**Set Up Celery for Background Tasks:**

Install Celery and configure it with Redis as the broker. Celery will be used to process tasks like:
Verifying transaction limits.
Sending email notifications (e.g., on transaction completion).

Celery is configured to work asynchronously so that transaction verification or notifications do not block the main application flow.

**Install Dependencies: Install all required libraries for the project:**

Used a requirements.txt file where I had all the dependancies and libraries

Django==5.0.3

djangorestframework==3.15.1

psycopg2-binary==2.9.9

djangorestframework-simplejwt==5.3.1

celery

redis

python-decouple==3.8

To install all run

pip install -r requiremets.txt

**Configure Celery and JWT in Django Settings**

Celery: Set up the Celery configuration to connect with Redis as the broker.

JWT Authentication: Add settings in Django’s REST Framework to use JWT authentication.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

**Set Up Docker**

Dockerfile: Create a Dockerfile for building the Django app container. This will include installing dependencies, 

setting up the environment, and exposing the required ports.

docker-compose.yml: Set up Docker Compose to orchestrate the services (Django, PostgreSQL, Redis).

The docker-compose.yml file will include services for:

db: PostgreSQL database service.

web: Django application service.

redis: Redis service used by Celery.

**Running the Application**

Build and Run the Docker Containers:

From the project directory, build and run the containers using Docker Compose:

docker-compose up --build -d

**Apply Migrations:**

Apply database migrations to set up the schema for the User Account and Transaction models:

docker-compose exec web python manage.py migrate

**Create a Superuser**

Create an admin superuser to access the Django admin panel:

docker-compose exec web python manage.py createsuperuser


**Access the App**

The application will be running at http://localhost:8000/.
You can use tools like Postman or curl to test the API endpoints:
User Registration: POST to /register/ with user details.
User Login: POST to /login/ with credentials (to get a JWT token).
Transaction Initiation: POST to /transactions/ to create a new transaction.
Transaction History: GET to /transactions/ to view all transactions for the logged-in user.

**Testing the Endpoints** 

User Registration:

POST /register/ with user details (first name, last name, email, password).

On success, a JWT token is returned.
User Login:

POST /login/ with email and password.
On success, a JWT token is returned for subsequent API requests.
Initiate a Transaction:

POST /transactions/ with details like amount, transaction type (deposit/withdrawal/transfer), and the recipient (if applicable).

View Transactions:

GET /transactions/ to view all transactions for the authenticated user.

**Role-based Access Control**

Implement role-based access using Django groups or custom permissions to restrict certain actions:

Admin users can view all transactions.
Regular users can only view their own transactions.
Only users with specific roles can perform certain types of transactions (e.g., admins for transfers).

**Cleanup**

After testing and development, you can stop the services:
docker-compose down

To clean up Docker volumes:

docker-compose down -v










