from fastapi import HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_NAME = "Innovation.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_NAME}"

engine = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

Base = declarative_base()


class SQLiteConnection:
    """
    Class to connect with Sqllite Database
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQLiteConnection, cls).__new__(cls)
            cls._instance.engine = engine
            cls._instance.SessionLocal = SessionLocal
        return cls._instance

    async def init_db(self):
        async with self.engine.begin() as conn:
            try:
                print("Creating tables...")
                await conn.run_sync(Base.metadata.create_all)
                print("Tables created successfully!")
            except HTTPException as e:
                print(f"Error creating tables: {e}")

    def get_session(self) -> AsyncSession:
        return self.SessionLocal()
