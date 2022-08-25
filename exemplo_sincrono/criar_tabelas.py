from os import sync
from core.async_form.configs import settings
from core.database import engine

async def create_tables() -> None:
    import exercicio.models.__all_models

    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run:sync(settings.DBBaseModel.metadata.create_all)

if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())