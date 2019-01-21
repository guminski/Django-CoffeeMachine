# Django Coffee Machine

Simple OOP coffee maker simulator written in Django

## Installing

**Clone repository**

Install dependencies by virtualenv

```
virtualenv -p python3.6 envname
source envname/bin/activate
pip install -r requirements.txt
```

**Create your .env file in same path as manage.py file.**
ENV file example template:
```
SECRET_KEY='YOURSECRETKEY'
DEBUG=True
ENVIRONMENT=development
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Run migrations:**
```
./manage.py migrate
```

**Run app:**
```
./manage.py runserver
```

## Running the tests

**TODO: Create tests :)**

