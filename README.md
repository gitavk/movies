# Movie demo app
## work using docker
### run application
```
make up-app
```
### run tests
```
make run-tests
```
## work locally
### setup development environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt
cp env.example .env
```
### run application
```
python -m uvicorn src.main:app --reload
```
### run tests
```
pytest --cov-report=term-missing --cov=src -p no:cacheprovider tests
```
### linting and code formatting check
```
make lint-local
```
### linting and code formatting auto fix (be careful run tests)
```
make fix-local
```

## How to improve current solution.
1. Tests:
* mock httpx and cover init db script
* pay more attention to data quality
* add integration tests to cover crud operations
2. Improve omdbapi parser and store data using relations instead JSON field.
3. Create User model instead hard code dictionary.
4. Configure Docker and docker compose for better using start.sh

