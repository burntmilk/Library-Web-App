import pytest
from flask import session


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data


def test_browse(client):   # test browse all books page
    response = client.get('browse')
    assert response.status_code == 200
    assert b'Browse Books' in response.data
    assert b'The Switchblade Mamma' in response.data
    assert b'Page 1' in response.data


def test_browse_page_num(client):   # test browse all books page with page num
    response = client.get('browse?page=2')
    assert response.status_code == 200
    assert b'Browse Books' in response.data
    assert b'Page 2' in response.data


def test_book(client):
    book_id = 30128855
    response = client.get('/book/30128855')
    assert response.status_code == 200
    assert b'Cruelle' in response.data

