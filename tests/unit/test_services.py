import pytest
from library.browse import services as browse_services
from library.authentication import services as auth_services
from library.authentication.services import AuthenticationException


def test_can_get_book(in_memory_repo):
    book_id = 30128855
    book_as_dict = browse_services.get_book(book_id, in_memory_repo)

    assert book_as_dict['book_id'] == 30128855
    assert book_as_dict['title'] == "Cruelle"
    assert book_as_dict['publisher'] == "Dargaud"
    assert book_as_dict['authors'] == [{'author_id': 3274315, 'full_name': 'Florence Dupre la Tour'}]
    assert book_as_dict['release_year'] == 2016
    assert book_as_dict['ebook'] is False
    assert book_as_dict['num_pages'] is None


def test_cannot_get_invalid_id_book(in_memory_repo):
    book_id = -1
    with pytest.raises(browse_services.NonExistentBookException):
        browse_services.get_book(book_id, in_memory_repo)


def test_can_get_all_books(in_memory_repo):
    books = browse_services.get_all_books(in_memory_repo)
    assert len(books) == 20


def test_can_get_book_stock(in_memory_repo):
    book_id = 30128855
    stock = browse_services.get_book_stock(book_id, in_memory_repo)
    assert stock == 0


def test_cannot_get_invalid_book_stock(in_memory_repo):
    book_id = -1
    with pytest.raises(browse_services.NonExistentBookException):
        browse_services.get_book_stock(book_id, in_memory_repo)


def test_can_get_book_price(in_memory_repo):
    book_id = 30128855
    price = browse_services.get_book_price(book_id, in_memory_repo)
    assert price == 0


def test_cannot_get_invalid_book_price(in_memory_repo):
    book_id = -1
    with pytest.raises(browse_services.NonExistentBookException):
        browse_services.get_book_price(book_id, in_memory_repo)

