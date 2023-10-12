from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./kaia.db", echo=True, future=True)

session = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)()

def connect():
    conn = session

    try:
        yield conn
    finally:
        conn.close()

