import pytest
from rest_framework import status
from django.urls import reverse
from moviecollection.models import Collection, User
from uuid import UUID

collection_field_mapping = {
    "title": "Test Collection",
    "description": "My Movies",
    "movies": [
        {
            "title": "Test Movie",
            "description": "A mind-bending thriller",
            "genres": "Sci-Fi, Thriller",
            "movie_id": "cc51020f-1bd6-42ad-84e7-e5c0396435a1",
        }
    ],
}


@pytest.mark.django_db
def test_collection_list_post(authenticated_client):
    url = reverse("collection_list")
    collection_field_mapping.update({"user": authenticated_client.auth["user_id"]})
    response = authenticated_client.post(url, collection_field_mapping, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "collection_id" in response.data
    assert isinstance(response.data["collection_id"], UUID)


# @pytest.mark.skip
@pytest.mark.django_db
def test_collection_list_get(authenticated_client):
    url = reverse("collection_list")
    test_collection_list_post(authenticated_client)
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["is_success"] is True
    assert len(response.data.get("data", [])) > 0
    assert (
        response.data.get("data", [])[0].get("title")
        == collection_field_mapping["title"]
    )


@pytest.mark.django_db
def test_get_collection_detail(authenticated_client):
    test_collection_list_get(authenticated_client)
    response = authenticated_client.get(reverse("collection_list"))
    url = reverse(
        "collection_detail", args=[response.data.get("data", [])[0].get("id")]
    )
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    assert response.data["id"] == response.data.get("id")
    assert response.data["title"] == response.data.get("title")
    assert response.data.get("movies")


# @pytest.mark.skip
@pytest.mark.django_db
def test_put_collection_detail(authenticated_client):
    test_collection_list_get(authenticated_client)
    response = authenticated_client.get(reverse("collection_list"))
    url = reverse(
        "collection_detail", args=[response.data.get("data", [])[0].get("id")]
    )
    collection_field_mapping.update({"title": "Updated Collection Name"})
    response = authenticated_client.put(url, collection_field_mapping, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Collection Name"


# @pytest.mark.skip
@pytest.mark.django_db
def test_delete_collection_detail(authenticated_client):
    test_collection_list_get(authenticated_client)
    response = authenticated_client.get(reverse("collection_list"))
    id = response.data.get("data", [])[0].get("id")
    url = reverse("collection_detail", args=[id])
    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Collection.objects.filter(id=id).exists()
