from app.database.connection import engine
from app.database.models import Base


def init_db():
    Base.metadata.create_all(bind=engine)
    print("DB tables ensured (created if missing)")
