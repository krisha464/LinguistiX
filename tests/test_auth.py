import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.storage import hash_password, verify_password, find_user


def test_find_user_and_verify_password():
    users = {
        'demo': {'password': hash_password('demo123'), 'email': 'demo@example.com'},
        'other': {'password': hash_password('secret'), 'email': 'other@example.com'},
    }

    username, data = find_user('demo', users)
    assert username == 'demo'
    assert data is not None
    assert verify_password('demo123', data['password']) is True
    assert verify_password('wrong', data['password']) is False
