from sqlalchemy import create_engine
from app.models.models import Base

# to test database connection
DATABASE_URL = "mysql://blog_user:admin@localhost/blog_db"
engine = create_engine(DATABASE_URL)

try:
    # try to create all tables
    Base.metadata.create_all(bind=engine)
    print("Database connection successful!")
    print("Tables created successfully!")
except Exception as e:
    print("Error:", e) 