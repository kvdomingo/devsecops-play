from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    "sqlite+aiosqlite:///./app.db",
    future=True,
    echo=True,
)

session_maker = async_sessionmaker(
    bind=engine,
    autoflush=True,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db():
    session = session_maker()
    try:
        yield session
    except DatabaseError as err:
        print(err)
        raise
    finally:
        await session.close()
