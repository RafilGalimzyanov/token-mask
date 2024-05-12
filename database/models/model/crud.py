from sqlalchemy.exc import IntegrityError

from database.core import handle_database_exception
from database.models import ModelORM, UserTokenModelORM


@handle_database_exception
def add_model(session, name):
    try:
        model = ModelORM(name=name)
        session.add(model)
        session.commit()

        return session.query(ModelORM).filter_by(name=name).first()

    except IntegrityError:
        session.rollback()

        raise ValueError(f"Model with name '{name}' already exists.")


@handle_database_exception
def get_models(session):
    return session.query(ModelORM).all()


@handle_database_exception
def delete_model(session, name):
    model = session.query(ModelORM).filter_by(name=name).first()

    if model:
        session.delete(model)
        session.query(UserTokenModelORM).filter_by(model_id=model.id).delete()
        session.commit()

    else:
        raise ValueError(f"Model with name '{name}' not found.")
