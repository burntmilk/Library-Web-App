from sqlalchemy import select, inspect
from library.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'favourites', 'publishers', 'reviews', 'users']


def test_database_populate_select_all_authors(database_engine):
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)
        all_author_ids = []
        for row in result:
            all_author_ids.append(row['id'])
        print(all_author_ids)
        assert len(all_author_ids) == 31


def test_database_populate_select_all_books(database_engine):
    inspector = inspect(database_engine)
    name_of_books_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)
        all_book_ids = []
        for row in result:
            all_book_ids.append(row['id'])
        print(all_book_ids)
        assert len(all_book_ids) == 20


def test_database_populate_select_all_publishers(database_engine):
    inspector = inspect(database_engine)
    name_of_publishers_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_publishers_table]])
        result = connection.execute(select_statement)
        all_publisher_ids = []
        for row in result:
            all_publisher_ids.append(row['id'])
        print(all_publisher_ids)
        assert len(all_publisher_ids) == 12
