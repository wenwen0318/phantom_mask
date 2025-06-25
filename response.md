# Response

## A. Required Information
### A.1. Requirement Completion Rate
- [o] List all pharmacies open at a specific time and on a day of the week if requested.
  - Implemented at `routes/pharmacy.py`.
- [o] List all masks sold by a given pharmacy, sorted by mask name or price.
  - Implemented at `routes/pharmacy.py`.
- [o] List all pharmacies with more or less than x mask products within a price range.
  - Implemented at `routes/pharmacy.py`.
- [o] The top x users by total transaction amount of masks within a date range.
  - Implemented at `routes/users.py`.
- [o] The total number of masks and dollar value of transactions within a date range.
  - Implemented at `routes/purchase.py`.
- [o] Search for pharmacies or masks by name, ranked by relevance to the search term.
  - Implemented at `routes/search.py`.
- [o] Process a user purchases a mask from a pharmacy, and handle all relevant data changes in an atomic transaction.
  - Implemented at `routes/purchase.py`.
### A.2. API Document

Import [this](#api-document) json file to Postman.

### A.3. Import Data Commands
Please run these script command to migrate the data into the database.

```bash
$ python app/init_db.py
```
## B. Bonus Information

>  If you completed the bonus requirements, please fill in your task below.
### B.1. Test Coverage Report

I wrote down the 20 unit tests for the APIs I built. Please check the test coverage report at [here](#test-coverage-report).

You can run the test script by using the command below:

```bash
bundle exec rspec spec
```

### B.2. Dockerized
Please check my Dockerfile / docker-compose.yml at [here](#dockerized).

On the local machine, please follow the commands below to build it.

```bash
$ docker build --build-arg ENV=development -p 80:3000 -t my-project:1.0.0 .  
$ docker-compose up -d

# go inside the container, run the migrate data command.
$ docker exec -it my-project bash
$ rake import_data:pharmacies[PATH_TO_FILE] 
$ rake import_data:user[PATH_TO_FILE]
```

### B.3. Demo Site Url

The demo site is ready on [my AWS demo site](#demo-site-url); you can try any APIs on this demo site.

## C. Other Information

### C.1. ERD

My ERD [erd-link](#erd-link).

### C.2. Technical Document

For frontend programmer reading, please check this [technical document](technical-document) to know how to operate those APIs.

- --
