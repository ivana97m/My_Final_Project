### 💻 Local Execution

To run the project locally, follow these steps:

📦 Requirements
- Python 3.14+
- uv - Fast Python package manager
- Dependencies defined in pyproject.toml


#### install uv (https://docs.astral.sh/uv/#highlights)
```powershell
curl -LsSf https://astral.sh/uv/install.sh | sh 
```

#### create pyprojec.toml file
```powershell
uv init
```

#### add new dependency (example)
```powershell
uv add fastapi
uv add uvicorn
uv add sqlalchemy
 ```

#### synchronize the dependencies, update uv lock file (uv.lock)

```powershell
uv sync
```

#### check if main.py is working
```powershell
uvicorn app.main:app --reload
```
#### build images and start containers
```powershell
docker compose up --build
```
#### stop containers
```powershell
docker compose down
```
####  to run all tests use pytest
```powershell
pytest
```
#### to run tests for a specific file
```powershell
uv run pytest tests/unit/test_security.py -v
```
