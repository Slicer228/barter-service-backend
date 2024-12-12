from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import DBurl


engine = create_async_engine(DBurl)

async_session_maker = sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)



