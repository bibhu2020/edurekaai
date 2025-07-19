# FASTAPI
FastAPI is a modern Python web framework used for building APIs quickly. It's fast, async-ready, and automatically generates interactive API docs using Swagger and ReDoc. It's built on Starlette (for web) and Pydantic (for data validation).

# Required Packages
```
pip install fastapi uvicorn

```

# Run the FASTAPI server
```
uvicorn main:app --reload

```

# A simple API
```python
from pydantic import BaseModel
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    return {"message": f"Item {item.name} created", "item": item}

```

# pydantic library
Pydantic models are classes that inherit from BaseModel provided by the Pydantic library. They are used in FastAPI to:
- define dto (data transfer objects) which defines schema, performs validation, and serialization/de-serialization.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than zero')
        return v

@app.post("/items/")
def create_item(item: Item):
    return {"received_item": item}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None, limit: int = 10):
    return {"item_id": item_id, "q": q, "limit": limit}
```

# ORM: SQLAlchemy
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

```

# Using MVC
```
app/
├── main.py
├── controllers/
│   └── user_controller.py
├── models/
│   ├── user.py
│   └── user_orm.py
├── services/
│   └── user_service.py
├── views/
│   └── templates/
│       └── user.html
├── database.py

```

```python (MODEL)
# models/user.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str


# models/user_orm.py
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)

```

```python (database connector)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

```

```python (CONTROLLER)

# controllers/user_controller.py
from fastapi import APIRouter, Depends
from models.user import UserCreate
from services.user_service import create_user

router = APIRouter()

@router.post("/users")
def create(user: UserCreate):
    return create_user(user)

```

```python (SERVICE)
# services/user_service.py
def create_user(user):
    # process and save user
    return {"message": f"User {user.username} created"}

```

```python (VIEW)
# views/templates/user.html
<h1>Hello, {{ username }}!</h1>

```

```python (main.py) - startup file
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from controllers import user_controller  # Make sure this exists
from database import engine, Base          # Your SQLAlchemy base and engine

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="FastAPI MVC Example")

# Enable CORS (optional, adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(user_controller.router, prefix="/api", tags=["Users"])

# Optional: Set up Jinja2 templates if serving HTML views
templates = Jinja2Templates(directory="views/templates")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

```

# fastapi vs django vs flask
