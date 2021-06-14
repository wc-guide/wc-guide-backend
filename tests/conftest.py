import json
import os
import uuid

import pytest

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def toilets(file):
    file_path = os.path.join(DIR_PATH, file)
    with open(file_path) as json_file:
        return json.load(json_file)


@pytest.fixture
def toilets_switzerland():
    return toilets('data/toilets_switzerland.geojson')


@pytest.fixture
def toilets_austria():
    return toilets('data/toilets_austria.geojson')


@pytest.fixture
def toilets_eurokey():
    return toilets('data/toilets_eurokey.geojson')


@pytest.fixture
def toilets_two():
    return toilets('data/toilets_two.geojson')


@pytest.fixture
def toilets_three():
    return toilets('data/toilets_three.geojson')


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login
