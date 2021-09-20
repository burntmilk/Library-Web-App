import pytest
from flask import session


def test_browse(client):
    response = client.get('browse')
    assert response.status_code == 200
    assert b'Browse Books' in response.data


def test_book(client):
    book_id = 30128855
    response = client.get()