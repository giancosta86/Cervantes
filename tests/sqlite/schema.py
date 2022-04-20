from contextlib import closing
from sqlite3 import Connection

ALL_TERMS_COUNT_QUERY = """
SELECT sum(total_set.partial_count) AS total
FROM
(
   SELECT count(*) AS partial_count FROM verbs
   UNION ALL
   SELECT count(*) AS partial_count FROM verb_forms
   UNION ALL
   SELECT count(*) AS partial_count FROM prepositions
   UNION ALL
   SELECT count(*) AS partial_count FROM articles
   UNION ALL
   SELECT count(*) AS partial_count FROM pronouns
   UNION ALL
   SELECT count(*) AS partial_count FROM adjectives
   UNION ALL
   SELECT count(*) AS partial_count FROM interjections
   UNION ALL
   SELECT count(*) AS partial_count FROM adverbs
   UNION ALL
   SELECT count(*) AS partial_count FROM nouns
   UNION ALL
   SELECT count(*) AS partial_count FROM conjunctions
) total_set;
"""


def count_terms_in_db(connection: Connection) -> int:
    with closing(connection.cursor()) as cursor:
        cursor.execute(ALL_TERMS_COUNT_QUERY)
        row = cursor.fetchone()
        return row[0]
