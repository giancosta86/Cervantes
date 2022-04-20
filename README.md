# Cervantes

_Extract a compact Spanish dictionary from Wikcionario, with elegance_

In Spanish literature - and all over the world - the works of [Miguel de Cervantes](https://en.wikipedia.org/wiki/Miguel_de_Cervantes) are considered an _obra maestra_ because of their stylistic 🦋elegance, witty remarks and _humanistic_ depth of thought...

...which is why I wish to dedicate this project to his memory: more precisely, this is my library for creating _a customized, Wiktionary-based corpus of the Spanish language_.

**Cervantes** is a type-checked library for Python, built on top of [WikiPrism](https://github.com/giancosta86/WikiPrism), focusing on:

- _Parsing_ an [XML dump](https://dumps.wikimedia.org/eswiktionary/latest/eswiktionary-latest-pages-articles.xml.bz2) of [Wikcionario](https://es.wiktionary.org/) and extracting _Spanish terms_ from each wiki page

- _Classifying_ each term according to a set of _grammar categories_

- Providing _a Spanish-related Dictionary_, backed by a SQLite db, that can be used for custom analysis via _SQL queries_

Despite its sophisticated _regex-based engine_, Cervantes has a minimalist programming interface; furthermore, it is designed to be a core plugin of [Jardinero](https://github.com/giancosta86/Jardinero) - which makes it extremely simple to use, via a web-application user interface.

No matter the scenario, it is essential to explore the SQL schema of its underlying database: for details, please consult the sections below.

## Installation

To install **Cervantes**, just run:

> pip install info.gianlucacosta.cervantes

or, if you are using Poetry:

> poetry add info.gianlucacosta.cervantes

## Extracting a custom dictionary from Wikcionario

Once Cervantes is installed in your Python environment, you can import it just like any other Python library - or you can run it within Jardinero's infrastructure!

In the latter case, make sure [Jardinero](https://github.com/giancosta86/Jardinero) is installed, then run:

> python \[-OO\] -m info.gianlucacosta.jardinero info.gianlucacosta.cervantes

If you start Jardinero with the **-OO** flag:

- the process will run slightly faster, but with less logging

- Jardinero will download the very latest dump from Wikcionario's official download website

On the other hand, if you omit the flag:

- you'll be able to see more logging messages

- Jardinero will use your local copy of Wikcionario's dump - that **must** be a BZ2 archive residing at the following address: **http://localhost:8000/eswiktionary-latest-pages-articles.xml.bz2**. In particular, this address becomes accessible once you run:

  > python -m http.server

  from the directory containing your downloaded - and maybe customized - [Wikcionario dump file](https://dumps.wikimedia.org/eswiktionary/latest/eswiktionary-latest-pages-articles.xml.bz2).

## Database schema

Every single table in the database created by Cervantes has two fields:

- **entry** (TEXT NOT NULL) - denoting the term within the dictionary

- **pronunciation** (TEXT) - the IPA pronunciation, with an ASCII apostrophe character (and not a more sophisticated Unicode symbol) before the syllable having the primary stress

Given the nature of the extraction process, there are no foreign keys enforcing consistency between tables (for example, between **verbs** and **verb_forms**) - but one can still perform JOINs according to one's needs.

### Table: prepositions

| Field         | Type | Required | Primary key |
| ------------- | ---- | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |

### Table: interjections

| Field         | Type | Required | Primary key |
| ------------- | :--: | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |

### Table: conjunctions

| Field         | Type | Required | Primary key |
| ------------- | :--: | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |

### Table: adverbs

| Field         | Type | Required | Primary key |
| ------------- | :--: | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |
| kind          | TEXT |          |     \*      |

### Table: verbs

| Field         | Type | Required | Primary key |
| ------------- | :--: | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |
| kind          | TEXT |          |     \*      |

### Table: pronouns

| Field         | Type | Required | Primary key |
| ------------- | :--: | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |
| kind          | TEXT |          |     \*      |

### Table: articles

| Field         | Type | Required | Primary key |
| ------------- | :--: | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |
| kind          | TEXT |          |     \*      |

### Table: adjectives

| Field           | Type | Required | Primary key |
| --------------- | :--: | :------: | :---------: |
| entry           | TEXT |    \*    |     \*      |
| pronunciation   | TEXT |          |             |
| reference_entry | TEXT |          |     \*      |

### Table: nouns

| Field           | Type | Required | Primary key |
| --------------- | :--: | :------: | :---------: |
| entry           | TEXT |    \*    |     \*      |
| pronunciation   | TEXT |          |             |
| gender          | TEXT |    \*    |     \*      |
| number_trait    | TEXT |          |             |
| reference_entry | TEXT |          |     \*      |

### Table: verb_forms

| Field         | Type | Required | Primary key |
| ------------- | :--: | :------: | :---------: |
| entry         | TEXT |    \*    |     \*      |
| pronunciation | TEXT |          |             |
| infinitive    | TEXT |    \*    |     \*      |
| mode          | TEXT |    \*    |     \*      |
| tense         | TEXT |          |     \*      |
| person        | TEXT |          |     \*      |

## The API

Even though this library is designed for [Jardinero](https://github.com/giancosta86/Jardinero), one can still use its functions in other Python programs - mostly in a custom subclass of [WikiPrism](https://github.com/giancosta86/WikiPrism)'s **PipelineStrategy**.

As a matter of fact, one just needs a few functions from the **info.gianlucacosta.cervantes** namespace:

- **extract_terms(page: Page) -> list\[SpanishTerm\]**: given a page, returns a list of Spanish terms from the page - and whose types can be imported from the **info.gianlucacosta.cervantes.terms** namespace. In WikiPrism's model, this function is a **TermExtractor\[SpanishTerm\]**

* **create_sqlite_dictionary(connection: Connection) -> SpanishSqliteDictionary**: given a SQLite connection, creates a **SqliteDictionary** (from WikiPrism) that will become its owner and that can be used to read and write Spanish terms. Consequently, it is a **SqliteDictionaryFactory\[SpanishTerm\]**

## Parting thoughts

**Cervantes** is a project that I created because I definitely needed to further explore Spanish morphology: actually, it was the initial kernel of [Jardinero](https://github.com/giancosta86/Jardinero), which I later refactored into a separate library, as well as [WikiPrism](https://github.com/giancosta86/WikiPrism).

Since it relies on a very dynamic source like Wikcionario, and despite the carefully-crafted parsing regular expressions, its output cannot be 100% accurate.

Furthermore, it focuses on the linguistic aspects that I felt more appealing according to my own needs - which means that I had to discard information during the parsing, or even to include aspects that may be unnecessary in a different context.

Consequently... feel free to experiment, and maybe to create your own library! ^\_\_^

Actually, one can even adopt Cervantes's patterns to create a linguistic module for Jardinero dedicated to another language! 🤩

## Further references

- [Jardinero](https://github.com/giancosta86/Jardinero) - Python/TypeScript React web app for exploring natural languages

- [WikiPrism](https://github.com/giancosta86/WikiPrism) - Parse wiki pages and create dictionaries, fast, with Python

* [Eos-core](https://github.com/giancosta86/Eos-core) - Type-checked, dependency-free utility library for modern Python

* [Miguel de Cervantes](https://en.wikipedia.org/wiki/Miguel_de_Cervantes)
