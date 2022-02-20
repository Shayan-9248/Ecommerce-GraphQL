# Ecommerce GraphQL

**This is a simple ecommerce app that implements with graphene django**

### Installation

__First download and install docker and docker-compose__

* [docker](https://docs.docker.com/engine/install/)
* [docker-compose](https://docs.docker.com/compose/install/)

#### Usage

```
    1.Create a .env file and add this three lines in it:
        * POSTGRES_USER='shayan'
        * POSTGRES_PASSWORD='shayan'
        * POSTGRES_DB='shayan'
    2.For bring the database up use the below command:
        * docker-compose up -d
    3. install all of the requirements package via command: pip install -r requirements.txt
    4. Run the following command to get the database ready to go:

        python manage.py migrate
```

*Now you can run the project with **python manage.py runserver** and this site will be available on localhost://8000*