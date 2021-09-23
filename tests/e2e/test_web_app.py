import pytest
from flask import session


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Library!' in response.data


def test_browse(client):   # test browse all books page
    response = client.get('browse')
    assert response.status_code == 200
    assert b'Browse books' in response.data
    assert b'The Switchblade Mamma' in response.data
    assert b'Page 1' in response.data


def test_browse_page_num(client):   # test browse all books page with page num
    response = client.get('browse?page=2')
    assert response.status_code == 200
    assert b'Browse books' in response.data
    assert b'Page 2' in response.data


def test_book(client):
    response = client.get('/book/30128855')
    assert response.status_code == 200
    assert b'Cruelle' in response.data


def test_filter_by_author_without_letter(client):   # shows all books until letter clicked
    response = client.get('/browse?filter=author')
    assert response.status_code == 200
    assert b'The Switchblade Mamma' in response.data
    assert b'Next Page' in response.data
    assert b'by author' in response.data


def test_filter_by_author_with_letter(client):
    response = client.get('/browse?filter=author&letter=A')
    assert response.status_code == 200
    assert b'The Thing: Idol of Millions' in response.data
    assert b'by author' in response.data


def test_filter_by_publisher_without_letter(client):    # shows all books until letter clicked
    response = client.get('/browse?filter=publisher')
    assert response.status_code == 200
    assert b'The Switchblade Mamma' in response.data
    assert b'Next Page' in response.data
    assert b'by publisher' in response.data


def test_filter_by_publisher_with_letter(client):
    response = client.get('/browse?filter=publisher&letter=A')
    assert response.status_code == 200
    assert b'War Stories, Volume 3' in response.data
    assert b'by publisher' in response.data


def test_filter_by_year_without_year(client):
    response = client.get('/browse?filter=year')
    assert response.status_code == 200
    assert b'The Switchblade Mamma' in response.data
    assert b'Next Page' in response.data
    assert b'by year' in response.data


def test_filter_by_year_with_year(client):
    response = client.get('/browse?filter=year&year=2016')
    assert response.status_code == 200
    assert b'Cruelle' in response.data
    assert b'by year' in response.data


def test_review(client, auth):
    client.post(
        '/authentication/register',
        data={'user_name': 'username', 'password': 'Password1'}
    )   # create existing user
    auth.login()
    response = client.post(
        '/review/30128855',
        data={'review_text': "test review", 'rating': 5, 'book_id': 30128855}
    )
    assert response.headers['Location'] == 'http://localhost/book/30128855'


def test_login_required_to_review(client):
    response = client.post('/review/30128855')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('review_text', 'messages'), (
        ('poop is a bad word', b'Your review must not contain profanity.'),
        ('so is pee', b'Your review must not contain profanity.')
))
def test_review_with_invalid_input(client, auth, review_text, messages):  # check against profanity
    client.post(
        '/authentication/register',
        data={'user_name': 'username', 'password': 'Password1'}
    )   # create existing user
    auth.login()
    response = client.post(
        '/review/30128855',
        data={'review_text': review_text, 'rating': 5, 'book_id': 30128855}
    )
    for message in messages:
        assert message in response.data


def test_register(client):
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    client.post(
        '/authentication/register',
        data={'user_name': 'fmercury', 'password': 'Test#6^0'}
    )   # create existing user first
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    client.post(
        '/authentication/register',
        data={'user_name': 'username', 'password': 'Password1'}
    )   # create existing user
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'username'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session
