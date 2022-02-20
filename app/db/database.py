from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.db.hashing import Hash

DATABASE_URL = (
    'postgresql+asyncpg://kefir:qwerty@localhost/kefir_db')

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, future=True
)

Base = declarative_base()

from app.db.models import User, City


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        async with session.begin():

            records = await session.scalar(func.count(User.id))

            if not records:
                session.add(User(first_name='Admin',
                                 city_ref=City(name='Moscow'),
                                 is_admin=True,
                                 email='admin@email.com',
                                 password=Hash.encrypt('secret')))

                await session.commit()
