### 💻 Local Execution

To run the project locally on Windows, follow these steps:

📦 Requirements
- Python 3.12+
- uv - Fast Python package manager
- Dependencies defined in pyproject.toml


#### install uv (https://docs.astral.sh/uv/#highlights)
```PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### create pyprojec.toml file
```PowerShell
uv init
```

#### add new dependency (example)
```PowerShell
uv add fastapi
uv add uvicorn
uv add sqlalchemy
 ```

#### Synchronize the dependencies, update uv lock file (uv.lock)

```PowerShell
uv sync
```

#### check if main.py is working
```PowerShell
uvicorn app.main:app --reload
```