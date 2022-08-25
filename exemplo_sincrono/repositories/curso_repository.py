import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status, HTTPException

from models.curso_model import CursoModel

# from app.util.logger import CloudWatchHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# logger.addHandler(CloudWatchHandler())

class CursosPostgree:
    
    def get_all_cursos(db: Session):
        try:
            logger.info('Iniciando query para buscar todos os cursos')
            cursos = db.query(CursoModel)
            logger.info('Retornando todas as notificações encontradas.')
            return cursos.all()
        
        except SQLAlchemyError as ex:
            logger.error(f'Erro ao buscar cursos no banco. Erro: {ex}')
            raise Exception(f'Erro ao buscar cursos no banco. Erro: {ex}')

    def get_curso(db: Session, id: int):
        try:
            logger.info('Iniciando query para buscar o curso')
            curso = db(CursoModel).with_entities(CursoModel.titulo,CursoModel.aulas,CursoModel.horas).filter(CursoModel.id == id)
            
            if curso:
                return curso.all()

            else:
                raise HTTPException(detail=f"curso não encontrado para o id: {id}", status_code=status.HTTP_404_NOT_FOUND)

        except SQLAlchemyError as ex:
            logger.error(f'Erro ao buscar notificações no admin: Erro: {ex}')
            raise Exception(f'Erro ao buscar notificações no admin: Erro: {ex}')

    def post_curso(db: Session, curso: CursoModel):

        try:
            novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas,horas=curso.horas)
            db.add(novo_curso)
            db.commit()

            return novo_curso
        
        except SQLAlchemyError as ex:
            logger.error(f'Erro ao inserir curso. Erro: {ex}')
            raise Exception(f'Erro ao inserir curso. Erro: {ex}')

    def put_curso(db: Session, curso: CursoModel, id: int):

        try:
            curso_update = CursoModel(titulo=curso.titulo, aulas=curso.aulas,horas=curso.horas)

            if curso_update:
                curso_update.titulo = curso.titulo
                curso_update.aulas = curso.aulas
                curso_update.horas = curso.horas

                db.refresh(curso_update)
 
            else:
                raise HTTPException(detail=f"curso não encontrado para o id: {id}", status_code=status.HTTP_404_NOT_FOUND)

        except SQLAlchemyError as ex:
            logger.error(f'Erro ao atualizar o curso: {id}. Erro: {ex}')
            raise Exception(f'Erro ao atualizar o curso: {id}. Erro: {ex}')
    
    def delete_item(db: Session, id: int):
        try:
            logger.info('Deletando curso no banco.')
            db_curso = db.query(CursoModel).filter(
                CursoModel.id == id
            ).one()

            db.commit()
            db.refresh(db_curso)
            return db_curso.id

        except SQLAlchemyError as ex:
            logger.error(f'Erro ao deletar curso {id}. Erro: {ex}')
            raise Exception(f'Erro ao deletar curso {id}. Erro: {ex}')