import json

import pytest

from django.urls import reverse

from guide.wc.models import Toilet, Other
from guide.wc.views import query_builder

CONTENT_TYPE = "application/json"


def create_or_update_area(auto_login_user, area, pk='area'):
    client, user = auto_login_user()
    url = reverse('area-detail', kwargs={'pk': pk})
    return client.put(url, json.dumps(area), content_type=CONTENT_TYPE)

def create_or_update_otherarea(auto_login_user, otherarea, pk='otherarea'):
    client, user = auto_login_user()
    url = reverse('otherarea-detail', kwargs={'pk': pk})
    return client.put(url, json.dumps(otherarea), content_type=CONTENT_TYPE)


@pytest.mark.django_db
def test_create_toilets_with_authenticated_client(auto_login_user, toilets_two):
    response = create_or_update_area(auto_login_user=auto_login_user, area=toilets_two)
    assert response.status_code == 201

    assert len(toilets_two['features']) == Toilet.objects.count()


@pytest.mark.django_db
def test_update_toilets_with_authenticated_client(auto_login_user, toilets_two, toilets_three):
    create_response = create_or_update_area(auto_login_user=auto_login_user, area=toilets_two)
    assert create_response.status_code == 201
    assert Toilet.objects.count() == 2

    update_response = create_or_update_area(auto_login_user=auto_login_user, area=toilets_three)
    assert update_response.status_code == 200
    assert Toilet.objects.count() == 3


@pytest.mark.django_db
def test_get_empty_toilets_with_authenticated_client(auto_login_user):
    client, user = auto_login_user()
    url = reverse('others-list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_toilets_in_bbox(auto_login_user, toilets_three):
    response = create_or_update_otherarea(auto_login_user=auto_login_user, otherarea=toilets_three)
    assert response.status_code == 201
    assert Other.objects.count() == 3

    client, user = auto_login_user()
    url = reverse('others-list')
    response = client.get(url, {'in_bbox': "0.0,25.0,25.0,0.0"})
    content = json.loads(response.content)
    assert len(content['results']['features']) == 2


def test_query_builder():
    bbox = [9, 47, 10, 48]
    query = query_builder(bbox)
    expected = '(node["amenity"="toilets"](47,9,48,10););out body;>;out skel qt;'
    assert query == expected
