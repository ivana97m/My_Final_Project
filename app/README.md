### 💻 Local Execution

To run the project locally, follow these steps:

📦 Requirements
- Python 3.12+
- uv - Fast Python package manager
- Dependencies defined in pyproject.toml


#### install uv (https://docs.astral.sh/uv/#highlights)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh 
```

#### create pyprojec.toml file
```bash
uv init
```

#### add new dependency (example)
```bash
uv add fastapi
uv add uvicorn
uv add sqlalchemy
 ```

#### Synchronize the dependencies, update uv lock file (uv.lock)

```bash
uv sync
```

#### check if main.py is working
```bash
uvicorn app.main:app --reload
```
#### docker kako se pokrece compose up i down, kako se pokrecu testovi uv run pytest....
3-layered architecture je način organizovanja koda gde se aplikacija deli na tri odvojena sloja, da bi kod bio čistiji, lakši za održavanje i testiranje.
Ta tri sloja su:

1. Presentation layer - ulaz u aplikaciju, mesto gde frontend komunicira sa backendom.
2. Business logic layer - ovde se nalazi logika aplikacije
3. Data access layer - ovaj sloj komunicira sa bazom

U modernom backendu slojevi su podeljeni na:
API  →  schemas  →  services  →  models  →  database

U našem slučaju:
Presentation layer
    API + schemas

Business layer
    services

Data layer
    models + database


Vizuelno

CLIENT
   │
   ▼
API endpoint
   │
   ▼
SCHEMA (validation)
   │
   ▼
SERVICE (business logic)
   │
   ▼
MODEL (database object)
   │
   ▼
DATABASE

Ovo se razdvaja da bi kod bio čitljiv, modularan, testabilan i skalabilan


1. schemas — struktura podataka za API

Definišu kako izgleda request i response API-ja i koriste Pydantic.
Primer iz koda:
class UserLoginRequest(BaseModel):
    login: str
    password: str

To znači da API očekuje JSON:
{
 "login": "ivana",
 "password": "12345"
}

Schemas - Definišu kako izgleda request i response API-ja, validiraju podatke, ne znaju ništa o bazi


2. models — struktura baze
Models definišu kako izgleda tabela u bazi. Koriste SQLAlchemy.
Primer:
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String)
    password_hash = Column(String)

3. services — biznis logika
Services je mesto gde se piše logika aplikacije. Sadrže logiku sistema, koriste models i koriste schemas


Primer - login korisnika

1. 
Request
POST /login

Client pošalje:

{
  "login": "ivana",
  "password": "12345"
}

2. schema

Koristi se schema UserLoginRequest iz schemas/users.py.

class UserLoginRequest(BaseModel):
    login: str
    password: str

FastAPI automatski parsira JSON, validira podatke, napravi Python objekat
Endpoint dobija data: UserLoginRequest

3. 
Endpoint poziva services
Endpoint može izgledati ovako:

@router.post("/login")
async def login(data: UserLoginRequest, db: DB):
    return await auth_service.login(db, data)

Sada se poziva service layer.
Service proverava korisnika, nađe usera u bazi, proveri password

Ako je login uspešan pravi se JWT, service poziva token = create_access_token({"sub": str(user.id)}). Token može da
izgleda ovako: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

Response schema:
TokenResponse

Client dobija:

{
 "access_token": "eyJhbGc...",
 "token_type": "bearer",
 "expires_in": 3600
}

CLIENT
   │
   │ POST /login
   ▼
API endpoint
   │
   ▼
Schema validation
(UserLoginRequest)
   │
   ▼
Service
(auth_service)
   │
   ▼
Database
(User model)
   │
   ▼
JWT token created
   │
   ▼
Client receives token
   │
   │ Authorization: Bearer token


Bazu ćemo napraviti preko docker-compose kao server app.
Zašto?
- svi developeri imaju istu bazu
- nema instalacije lokalno
- lako resetuješ bazu
- identično production okruženje
- PostgreSQL je server aplikacija.

Može da radi na tvom računaru, u Docker containeru, na cloud serveru
U tvom slučaju, pošto koristiš docker-compose, onda je baza u Docker containeru.
FastAPI se povezuje sa bazom koristeći SQLAlchemy preko DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/my_db"

Gde se čuvaju podaci baze?
Ako koristiš Docker compose sa volume:
volumes:
  - postgres_data:/var/lib/postgr