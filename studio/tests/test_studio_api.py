import pytest
from django.urls import reverse

from studio.models import Design, Master


def get_auth_client(api_client):
    login_url = reverse("token_obtain_pair")
    tokens = api_client.post(
        login_url,
        {"username": "adminuser", "password": "1234"},
        format="json",
    ).data
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    return api_client


@pytest.mark.django_db
def test_get_masters_list(api_client) -> None:
    Master.objects.create(name="Олена Корж", specialization="blackwork")
    response = api_client.get("/api/v1/masters", format="json")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_get_masters_empty_list(api_client) -> None:
    response = api_client.get("/api/v1/masters", format="json")
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_create_master_no_auth(api_client) -> None:
    response = api_client.post(
        "/api/v1/masters",
        {"name": "Олена Корж", "specialization": "blackwork"},
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_master_invalid_token(api_client) -> None:
    api_client.credentials(HTTP_AUTHORIZATION="Bearer invalidtoken")
    response = api_client.post(
        "/api/v1/masters",
        {"name": "Олена Корж", "specialization": "blackwork"},
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_master(api_client, user) -> None:
    client = get_auth_client(api_client)
    response = client.post(
        "/api/v1/masters",
        {"name": "Олена Корж", "specialization": "blackwork"},
        format="json",
    )
    assert response.status_code == 201
    assert response.data["name"] == "Олена Корж"


@pytest.mark.django_db
def test_create_master_invalid_data(api_client, user) -> None:
    client = get_auth_client(api_client)
    response = client.post(
        "/api/v1/masters",
        {"name": "", "specialization": "blackwork"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_master(api_client, user) -> None:
    master = Master.objects.create(name="Олена Корж", specialization="blackwork")
    client = get_auth_client(api_client)
    response = client.put(
        f"/api/v1/masters/{master.id}",
        {"name": "Олена Корж", "specialization": "dotwork"},
        format="json",
    )
    assert response.status_code == 200
    assert response.data["specialization"] == "dotwork"


@pytest.mark.django_db
def test_delete_master_with_designs_conflict(api_client, user) -> None:
    master = Master.objects.create(name="Олена Корж", specialization="blackwork")
    Design.objects.create(
        title="Мандала",
        style="blackwork",
        price=1500,
        image_url="https://example.com/1.jpg",
        master=master,
    )
    client = get_auth_client(api_client)
    response = client.delete(f"/api/v1/masters/{master.id}", format="json")
    assert response.status_code == 409


@pytest.mark.django_db
def test_delete_master_success(api_client, user) -> None:
    master = Master.objects.create(name="Олена Корж", specialization="blackwork")
    client = get_auth_client(api_client)
    response = client.delete(f"/api/v1/masters/{master.id}", format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_master_not_found(api_client) -> None:
    response = api_client.get("/api/v1/masters/9999", format="json")
    assert response.status_code == 404


@pytest.mark.django_db
def test_designs_crud_and_filter(api_client, user) -> None:
    master = Master.objects.create(name="Олена Корж", specialization="blackwork")
    client = get_auth_client(api_client)

    create_resp = client.post(
        "/api/v1/designs",
        {
            "title": "Мандала",
            "style": "blackwork",
            "price": 1500,
            "image_url": "https://example.com/1.jpg",
            "master": master.id,
        },
        format="json",
    )
    assert create_resp.status_code == 201
    design_id = create_resp.data["id"]

    list_resp = api_client.get("/api/v1/designs?style=blackwork", format="json")
    assert list_resp.status_code == 200
    assert len(list_resp.data) == 1

    update_resp = client.put(
        f"/api/v1/designs/{design_id}",
        {
            "title": "Мандала 2",
            "style": "blackwork",
            "price": 2000,
            "image_url": "https://example.com/1.jpg",
            "master": master.id,
        },
        format="json",
    )
    assert update_resp.status_code == 200
    assert update_resp.data["price"] == 2000

    delete_resp = client.delete(f"/api/v1/designs/{design_id}", format="json")
    assert delete_resp.status_code == 200
