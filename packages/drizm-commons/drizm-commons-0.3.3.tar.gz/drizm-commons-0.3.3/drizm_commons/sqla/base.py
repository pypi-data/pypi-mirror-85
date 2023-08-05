import weakref
from re import sub
from typing import Any

from sqlalchemy import MetaData, Integer, Column, Sequence
from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
    DeclarativeMeta
)


def gen_tablenames(name: str) -> str:
    """ Converts CamelCase class names to snake_case table names """
    return sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


class _declared_Base:
    @declared_attr
    def __tablename__(self) -> str:
        """ Automatically sets the name for created tables """
        return gen_tablenames(self.__name__)

    pk = Column(
        Integer(),
        Sequence("%(table_name)s_id_seq"),
        primary_key=True
    )


Base = declarative_base(
    cls=_declared_Base,
    metadata=MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",  # index
            "uq": "uq_%(table_name)s_%(column_0_name)s",  # unique constraint
            "ck": "ck_%(table_name)s_%(constraint_name)s",  # check constraint
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # foreign key
            "pk": "pk_%(table_name)s",  # primary key
        }
    ),
)


class Registry:
    def __init__(self, base) -> None:
        self._base = weakref.ref(base)
        self.tables = base._decl_class_registry  # noqa access to protected

    def table_class_from_tablename(self, tablename: str) -> DeclarativeMeta:
        base = self._resolve_weakref(self._base)
        assert issubclass(base, Base), \
            "This method attempts to reverse the automatic " \
            "naming done by this packages custom " \
            "declarative Base." \
            "When other baseclasses are used this process " \
            "does not work."
        refs = {
            gen_tablenames(c): c for c in self.tables.keys()
        }
        classname = refs[tablename]
        return self._resolve_weakref(self.tables[classname])

    # noinspection PyMethodMayBeStatic
    def _resolve_weakref(self, ref: weakref.ref) -> Any:
        return ref()

    def __getitem__(self, table_classname: str) -> DeclarativeMeta:
        table_ref = self.tables[table_classname]
        return self._resolve_weakref(table_ref)


__all__ = ["gen_tablenames", "Base", "Registry"]
