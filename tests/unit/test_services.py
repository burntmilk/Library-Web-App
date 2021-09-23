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


def test_can_add_review(in_memory_repo):
    book_id = 30128855
    review_text = "test review"
    rating = 5
    browse_services.add_review(book_id, review_text, rating, in_memory_repo)
    reviews_as_dict = browse_services.get_all_reviews_of_book(book_id, in_memory_repo)
    assert next(
        (dictionary['rating'] for dictionary in reviews_as_dict if dictionary['rating'] == rating),
        None) is not None


def test_cannot_add_review_for_invalid_book(in_memory_repo):
    book_id = -1
    review_text = "test review"
    rating = 5
    with pytest.raises(browse_services.NonExistentBookException):
        browse_services.add_review(book_id, review_text, rating, in_memory_repo)


def test_can_get_reviews_of_book(in_memory_repo):
    book_id = 30128855
    review_text = "test review"
    rating = 5
    browse_services.add_review(book_id, review_text, rating, in_memory_repo)
    reviews_as_dict = browse_services.get_all_reviews_of_book(book_id, in_memory_repo)
    assert len(reviews_as_dict) == 1


def test_cannot_get_reviews_of_invalid_book(in_memory_repo):
    book_id = -1
    review_text = "test review"
    rating = 5
    with pytest.raises(browse_services.NonExistentBookException):
        browse_services.get_all_reviews_of_book(book_id, in_memory_repo)


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'
    auth_services.add_user(new_user_name, new_password, in_memory_repo)
    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'
    auth_services.add_user(new_user_name, new_password, in_memory_repo)
    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'
    auth_services.add_user(new_user_name, new_password, in_memory_repo)
    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_get_books_by_author_initial(in_memory_repo):
    books_as_dict = browse_services.get_books_by_author_initial('a', in_memory_repo)
    assert len(books_as_dict) == 2
    assert books_as_dict[1]['title'] == "The Thing: Idol of Millions"


def test_can_get_empty_list_when_getting_books_by_author_initial(in_memory_repo):
    books = browse_services.get_books_by_author_initial('z', in_memory_repo)
    assert books == []


def test_can_get_books_by_publisher_initial(in_memory_repo):
    books_as_dict = browse_services.get_books_by_publisher_initial('a', in_memory_repo)
    assert len(books_as_dict) == 4
    assert books_as_dict[0]['publisher'] == "Avatar Press"


def test_can_get_empty_list_when_getting_books_by_publisher_initial(in_memory_repo):
    books = browse_services.get_books_by_publisher_initial('z', in_memory_repo)
    assert books == []


def test_can_get_book_years(in_memory_repo):
    years = browse_services.get_book_years(in_memory_repo)
    assert len(years) == 8
    assert years[0] == 1997
    assert years[1] == 2006
    for year in years:
        assert year is not None


def test_can_get_books_with_no_year(in_memory_repo):
    books = browse_services.get_books_with_no_year(in_memory_repo)
    assert len(books) == 4
    for book in books:
        assert book['release_year'] is None


def test_can_get_books_by_year(in_memory_repo):
    books_as_dict = browse_services.get_books_by_year(2016, in_memory_repo)
    assert len(books_as_dict) == 5


def test_can_get_empty_list_when_getting_books_by_year(in_memory_repo):
    books_as_dict = browse_services.get_books_by_year(-1, in_memory_repo)
    assert books_as_dict == []
