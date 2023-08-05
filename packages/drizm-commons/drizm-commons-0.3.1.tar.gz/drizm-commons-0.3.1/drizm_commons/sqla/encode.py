import datetime
import json
from typing import Any

from sqlalchemy import Table
from sqlalchemy.ext.declarative import DeclarativeMeta

from . import SQLAIntrospector


class SqlaDeclarativeEncoder(json.JSONEncoder):
    """
    A custom JSON encoder for serializing SQLAlchemy
    declarative base instances.

    Supports ISO8601 compliant datetime encoding.
    """
    datetypes = (
        datetime.date,
        datetime.datetime,
        datetime.timedelta
    )

    def default(self, o: Any) -> Any:
        # Check if the object is an SQLAlchemy declarative instance
        if isinstance(o.__class__, DeclarativeMeta):
            fields = {}
            # Get all fields of the class
            for field in SQLAIntrospector(o).column_attrs:
                data = self._process_column(o, field)
                fields[field] = data
            return fields

        # Or if it is an SQLAlchemy table instance
        elif isinstance(o, Table):
            fields = {}
            # Get all columns of the table
            for field in [c.key for c in SQLAIntrospector(o).columns]:
                data = self._process_column(o, field)
                fields[field] = data
            return fields

        # If it is not an SQLAlchemy object, use the default encoder
        return super(SqlaDeclarativeEncoder, self).default(o)

    def _process_column(self, o: Any, column_name: str):
        # Obtain the value of the column and check for custom encoding
        data = self.dump(
            getattr(o, column_name)
        )
        try:  # Try JSON encoding the field
            json.dumps(data)
        except TypeError as exc:  # if it fails resort to failure hook
            data = self.handle_failure(exc, data)
        return data

    def dump(self, v: Any) -> Any:
        """ Hook for custom object deserialization """
        if v.__class__ in self.datetypes:
            return self.serialize_datetypes_to_iso(v)
        return v

    # noinspection PyMethodMayBeStatic
    def serialize_datetypes_to_iso(self, v: datetypes) -> str:
        """ Converts datetime formats to ISO8601 compliant strings """
        if isinstance(v, datetime.timedelta):
            return (datetime.datetime.min + v).time().isoformat()
        return v.isoformat()

    def handle_failure(self, exc: Exception, value: Any):
        """ Can be overridden to provide handling for custom fields """
        # Simply re-raise the exception by default
        raise exc


__all__ = ["SqlaDeclarativeEncoder"]
