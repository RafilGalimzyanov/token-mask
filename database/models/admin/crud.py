from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status

from database.models.admin.model import AdminORM
from service.database_maker import get_db
from service.models import AdminDTO
from config import settings


def create_default_admin(session: Session):
    admin = session.query(AdminORM).filter(AdminORM.name == 'admin').first()

    if not admin:
        admin = AdminORM(name='admin', token=settings.admin.token)
        session.add(admin)
        session.commit()
        session.close()


async def get_admin(token: str, session: Session = Depends(get_db)) -> AdminDTO:
    admin = session.query(AdminORM).filter(AdminORM.token == token).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin not found with provided token")

    return AdminDTO(id=admin.id, name=admin.name, token=admin.token)
