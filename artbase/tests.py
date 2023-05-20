import pytest
from django.urls import reverse

from artbase.models import Category, StreetArt, Review


@pytest.mark.django_db
def test_street_art_detail(street_art, street_art_photo, review, client):
    url = f"/streetart/{street_art.pk}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["art"].title == street_art.title
    assert response.context["art"].artist == street_art.artist
    assert response.context["art"].year == street_art.year
    assert response.context["art"].description == street_art.description
    assert response.context["art"].category == street_art.category
    assert response.context["art_rating"] == review.rating
    assert list(response.context["reviews"]) == [review]
    assert response.context["reviews"][0].content == review.content
    assert list(response.context["photos"]) == [street_art_photo]
    # to return a QuerySet of single value => flat=True
    assert list(response.context["photos"].values_list("photo", flat=True)) == [
        street_art_photo.photo
    ]


@pytest.mark.django_db
def test_street_art_detail_not_found(client):
    url = "/streetart/9999/"
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_street_art_list_view(street_art, client):
    url = f"/streetart/list/"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["art_list"]) == 1
    assert response.context["art_list"][0]["art"].title == street_art.title
    assert response.context["art_list"][0]["art"].artist == street_art.artist
    assert response.context["art_list"][0]["art"].year == street_art.year
    assert response.context["art_list"][0]["art"].description == street_art.description
    assert response.context["art_list"][0]["art_rating"] == None
    assert response.context["art_list"][0]["number_of_reviews"] == 0
    assert list(response.context["art_list"][0]["photos"]) == []


@pytest.mark.django_db
def test_street_art_list_view_with_reviews(street_art, review, client):
    url = f"/streetart/list/"
    response = client.get(url)
    assert len(response.context["art_list"]) == 1
    assert response.context["art_list"][0]["art_rating"] == review.rating
    assert response.context["art_list"][0]["number_of_reviews"] == 1
    assert list(response.context["art_list"][0]["photos"]) == []


@pytest.mark.django_db
def test_street_art_list_view_with_photos(street_art_photo, client):
    url = f"/streetart/list/"
    response = client.get(url)
    assert len(response.context["art_list"]) == 1
    assert list(response.context["art_list"][0]["photos"]) == [street_art_photo]


@pytest.mark.django_db
def test_home_view_get_map(home_view, street_art, client):
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "map" in response.context
    assert isinstance(response.context["map"], str)
    assert "Test Art" in response.content.decode()


@pytest.mark.django_db
def test_login_view(client, user):
    response = client.get("/accounts/login/")
    assert response.status_code == 200

    # Sending POST request with valid authentication data and captcha verification
    response = client.post(
        "/accounts/login/",
        {
            "username": "test_user",
            "password": "test_pwd",
            "captcha": "PASSED",
            "captcha_0": "PASSED",
            "captcha_1": "PASSED",
        },
    )
    assert response.status_code == 302, response.context["form"].errors

    # Sending POST request with invalid credentials
    response = client.post(
        "/accounts/login/",
        {
            "username": "invalid_user",
            "password": "invalid_password",
            "captcha": "PASSED",
            "captcha_0": "PASSED",
            "captcha_1": "PASSED",
        },
    )

    assert response.status_code == 302, response.context["form"].errors

    # Sending POST request with correct authentication data but incorrect captcha verification
    response = client.post(
        "/accounts/login/",
        {
            "username": "test_user",
            "password": "test_pwd",
            "captcha": "PASSED",
            "captcha_0": "PASSED",
            "captcha_1": "FAILED",
        },
    )

    assert response.status_code == 302, response.context["form"].errors


@pytest.mark.django_db
def test_logout_view(client, user):
    response = client.get("/accounts/logout/")
    client.logout()

    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_street_art_view_post_valid(user, street_art, client):
    client.force_login(user)
    url = f"/streetart/{street_art.pk}/edit/"
    response = client.get(url)

    assert response.status_code == 200

    category = Category.objects.create(type=Category.ArtworkType.NEON)
    data = {
        "title": "Updated Art",
        "artist": "Updated Artist",
        "year": 2024,
        "description": "Updated Description",
        "category": category.pk,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    }
    response = client.post(url, data)

    assert response.status_code == 302

    updated_art = StreetArt.objects.get(pk=street_art.pk)

    assert updated_art.title == "Updated Art"
    assert updated_art.artist == "Updated Artist"
    assert updated_art.year == 2024
    assert updated_art.description == "Updated Description"


@pytest.mark.django_db
def test_edit_street_art_view_post_invalid(user, street_art, client):
    client.force_login(user)
    url = f"/streetart/{street_art.pk}/edit/"
    response = client.get(url)
    assert response.status_code == 200

    category = Category.objects.create(type=Category.ArtworkType.NEON)
    data = {
        "title": "",  # empty field
        "artist": "Updated Artist",
        "year": 2024,
        "description": "Updated Description",
        "category": category.pk,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    }
    response = client.post(url, data)

    assert response.status_code == 200  # form with errors
    assert "title" in response.context["form"].errors

    updated_art = StreetArt.objects.get(pk=street_art.pk)
    assert updated_art.title == street_art.title
    assert updated_art.artist == street_art.artist
    assert updated_art.year == street_art.year
    assert updated_art.description == street_art.description


@pytest.mark.django_db
def test_add_street_art_success(client, user):
    url = "/streetart/new/"
    client.force_login(user)
    category = Category.objects.create(type=Category.ArtworkType.MURAL)
    response = client.post(url, {
        "title": "Test Art",
        "artist": "Test Artist",
        "year": 2023,
        "description": "Test Description",
        "category": category.pk,
        "longitude": 19.02546,  # coordinates for Katowice (Spodek)
        "latitude": 50.26625,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })
    assert StreetArt.objects.count() == 1
    new_art = StreetArt.objects.get(title="Test Art")
    assert new_art.title == "Test Art"

    # Checking that the indicated coordinates point to Katowice
    assert new_art.location.city == "Katowice"
    assert response.status_code == 302, response.context["form"].errors


@pytest.mark.django_db
def test_add_street_art_fail(client, user):
    url = "/streetart/new/"
    client.force_login(user)
    category = Category.objects.create(type=Category.ArtworkType.MURAL)
    response = client.post(url, {
        "title": "",  # Empty field
        "artist": "Test Artist",
        "year": 2023,
        "description": "Test Description",
        "category": category.pk,
        "longitude": 19.02546,
        "latitude": 50.26625,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })

    assert response.status_code == 200  # form with errors
    assert StreetArt.objects.count() == 0


@pytest.mark.django_db
def test_create_new_review_view_success(client, user, street_art):
    url = f"/streetart/{street_art.pk}/review/new/"
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 200

    assert response.context["related_instance"] == street_art

    response = client.post(url, {
        "content": "Test content",
        "rating": 5,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })

    assert response.status_code == 302, response.context["form"].errors

    assert Review.objects.count() == 1
    review = Review.objects.first()
    assert review.content == "Test content"
    assert review.rating == 5
    assert review.art == street_art
    assert review.creator == user


@pytest.mark.django_db
def test_create_new_review_view_fail(client, user, street_art):
    url = f"/streetart/{street_art.pk}/review/new/"
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, {
        "content": "",  # Empty field
        "rating": 5,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })

    assert response.status_code == 200
    assert Review.objects.count() == 0


@pytest.mark.django_db
def test_update_review_view_success(client, user, street_art, review):
    url = f"/streetart/{street_art.pk}/reviews/{review.pk}/"
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, {
        "content": "Updated content",
        "rating": 4,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })

    assert response.status_code == 302, response.context["form"].errors

    updated_review = Review.objects.get(pk=review.pk)
    assert updated_review.content == "Updated content"
    assert updated_review.rating == 4
    assert updated_review.art == street_art
    assert updated_review.creator == user


@pytest.mark.django_db
def test_update_review_view_fail(client, user, street_art, review):
    url = f"/streetart/{street_art.pk}/reviews/{review.pk}/"
    client.force_login(user)

    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, {
        "content": "",  # Empty field
        "rating": 4,
        "captcha": "PASSED",
        "captcha_0": "PASSED",
        "captcha_1": "PASSED",
    })

    assert response.status_code == 200
    assert Review.objects.get(pk=review.pk) == review
    assert review.content == 'Test Review'
    assert review.rating == 5
