from typing import List
import logging

from fastapi import APIRouter, status, Depends, Request
from models.curso_model import CursoModel
from sqlalchemy.orm import Session
from core.database import engine, Base
from core.deps import get_session
from repositories import curso_repository
from util.make_response import make_response

router = APIRouter()

# vi para criar um arquivo criar tabela
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# podemos puxar pelo status.HTTP?
@router.get('/',status_code=status.HTTP_200_OK, response_model=List[CursoModel])
def get_cursos(request: Request, db: Session = Depends(get_session)):

    try:
        cursos = curso_repository.CursosPostgree.get_all_cursos(db)
        
        if not cursos:
            logger.error('Nenhum curso cadastrado.')
            return make_response(request, status_code=status.HTTP_404_NOT_FOUND, message='Nenhum curso cadastrado.')
            
        logger.info(f'Retornando os cursos.')
        return make_response(request, status_code=status.HTTP_200_OK, data=cursos)
        
    except Exception as ex:
        logger.error(f'{ex}')
        return make_response(request, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'{ex}')


@router.get('/{id}', response_model=CursoModel, status_code=status.HTTP_200_OK)
def get_curso(request: Request, id: int, db: Session = Depends(get_session)):
    try:
        curso = curso_repository.CursosPostgree.get_curso(db, id)
        
        if not curso:
            logger.error(f'Nenhum curso cadastrado para o id: {id}')
            return make_response(request, status_code=status.HTTP_404_NOT_FOUND, message=f'Nenhum curso cadastrado para o id: {id}.')
            
        logger.info(f'Retornando os cursos.')
        return make_response(request, status_code=status.HTTP_200_OK, data=curso)
        
    except Exception as ex:
        logger.error(f'{ex}')
        return make_response(request, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'{ex}')

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CursoModel)
def post_curso(request: Request, curso:CursoModel, db: Session = Depends(get_session)):
    novo_curso = curso_repository.CursosPostgree.post_curso(db, curso)
    try:
        if not novo_curso:
            logger.error(f'Não foi enviado um curso a ser cadastrado')
            return make_response(request, status_code=status.HTTP_404_NOT_FOUND, message=f'Não foi enviado um curso a ser cadastrado.')
                
        logger.info(f'Retornando o novo curso criado.')
        return make_response(request, status_code=status.HTTP_201_CREATED, data=novo_curso)

    except Exception as ex:
        logger.error(f'{ex}')
        return make_response(request, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'{ex}')

@router.put('/{id}', response_model=CursoModel, status_code=status.HTTP_202_ACCEPTED)
def put_curso(request: Request, id: int, curso:CursoModel, db: Session = Depends(get_session)):

    curso_update = curso_repository.CursosPostgree.put_curso(db, curso)
    try:
        if not curso_update:
            logger.error(f'Não foi enviado um curso a ser atualizado')
            return make_response(request, status_code=status.HTTP_404_NOT_FOUND, message=f'Não foi enviado um curso a ser atualizado.')
                
        logger.info(f'Retornando o curso atualizado.')
        return make_response(request, status_code=status.HTTP_202_ACCEPTED, data=curso_update)

    except Exception as ex:
        logger.error(f'{ex}')
        return make_response(request, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'{ex}')

@router.delete("/{id}", response_model=CursoModel, status_code=status.HTTP_200_OK)
def delete_curso(request: Request, id: int, curso:CursoModel, db: Session = Depends(get_session)):
    curso_delete = curso_repository.CursosPostgree.delete_item(db, id)
    try:
        if not curso_delete:
            logger.error('Não foi possivel deletar o curso.')
            return make_response(request, status_code=status.HTTP_404_NOT_FOUND, message='Não foi possivel deletar o curso.')
                
        logger.info(f'Retornando o curso atualizado.')
        return make_response(request, status_code=status.HTTP_202_ACCEPTED, data=curso_delete)

    except Exception as ex:
        logger.error(f'{ex}')
        return make_response(request, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'{ex}')
