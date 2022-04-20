from sqlite3 import Connection

from info.gianlucacosta.wikiprism.dictionary.sqlite import SqliteDictionary

from ..terms import SpanishTerm
from .schema import create_spanish_schema
from .serializers import create_spanish_serializer


class SpanishSqliteDictionary(SqliteDictionary[SpanishTerm]):
    def __init__(self, connection: Connection) -> None:
        super().__init__(connection=connection, serializer_factory=create_spanish_serializer)

    def create_schema(self) -> None:
        create_spanish_schema(self._connection)
