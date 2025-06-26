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
$ python run_etl.py
```
## B. Bonus Information

## C. Other Information

### C.1. ERD

[My ERD](docs\ERD.png).

### C.2. Technical Document

For frontend programmer reading, please check this [api_docs](docs\api_docs.md) to know how to operate those APIs.

- --
