from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
import datetime

from ._configuration import interception_config

__all__ = [
    'new_session',
    'Interception',
    'InterceptionVars'
]

Base = declarative_base()


class Interception(Base):
    __tablename__ = 'INTERCEPTION'

    id = Column(Integer, primary_key=True, name="id")
    ps = Column(String, name="ps")
    x = Column(String, name="x")
    trace = Column(String, name="trace")
    name = Column(String, name="name")
    created_at = Column(DateTime, name="created_at")

    def __repr__(self):
        return f'<Interception(id={self.id}, ps={self.ps}, x={self.x}, trace={self.trace}, name={self.name})>'

    @staticmethod
    def of(ps, x, trace, name):
        interception = Interception()
        interception.ps = ps
        interception.name = name
        interception.trace = trace
        interception.x = x
        interception.created_at = datetime.datetime.now()
        return interception


class InterceptionVars(Base):
    __tablename__ = 'INTERCEPTION_VARS'

    id = Column(Integer, primary_key=True, name="id")
    active = Column(Integer, name="active")


def new_session():
    engine = create_engine(interception_config.connection_string)
    session_cls = sessionmaker(bind=engine)
    return session_cls()
