from typing import Generator
from fastapi import HTTPException, status
from database import LocalSession

# vale a pena usar o generator?
def get_session() -> Generator:
    session = LocalSession()

    try:
        yield session
    
    except Exception as ex:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao realizar conexão. Erro: {ex}")
    
    finally:
        session.close()
