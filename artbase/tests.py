import pytest

from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_street_art_detail(street_art, street_art_photo, review, client):
    url = f"/streetart/{street_art.pk}/"
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['art'].title == street_art.title
    assert response.context['art'].artist == street_art.artist
    assert response.context['art'].year == street_art.year
    assert response.context['art'].description == street_art.description
    assert response.context['art'].category == street_art.category
    assert response.context['art_rating'] == review.rating
    assert list(response.context['reviews']) == [review]
    assert response.context['reviews'][0].content == review.content
    assert list(response.context['photos']) == [street_art_photo]
    # to return a QuerySet of single value => flat=True
    assert list(response.context['photos'].values_list('photo', flat=True)) == [street_art_photo.photo]


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
def test_home_view_get_map(home_view, street_art):
    client = Client()
    response = client.get(reverse("home"))
    assert response.status_code == 200
    assert "map" in response.context
    assert isinstance(response.context["map"], str)
    assert "Test Art" in response.content.decode()

# Nieudane próby napisania testów

# @pytest.mark.django_db
# def test_login_view(client, user):
#     # TU TEŻ NIE PRZECHODZI BO MNIE NIE UWIERZYTELNIA
#     response = client.post("/accounts/login/", {"username": "test_user", "password": "test_pwd", "captcha": True})
#     assert response.status_code == 200  # Sprawdzanie przekierowania do strony głównej po poprawnym uwierzytelnieniu i zalogowaniu
#
#     response = client.post("/accounts/login/", {"username": "invalid_user", "password": "invalid_password", "captcha": True})
#     assert response.status_code == 400  # Sprawdzanie kodu statusu przy niepoprawnych danych logowania
#
#     response = client.post("/accounts/login/", {"username": "test_user", "password": "test_pwd", "captcha": False})
#     assert response.status_code == 400  # Sprawdzanie kodu statusu przy niepoprawnej weryfikacji captcha
#


# @pytest.mark.django_db
# def test_edit_street_art_view_post_valid(user, street_art, client):
#     client.login(username="test-user", password="test-pwd")
#     url = f"/streetart/{street_art.pk}/edit/"
#     response = client.get(url)
#     assert response.status_code == 200
#
#     category = Category.objects.create(type=Category.ArtworkType.NEON)
#     data = {
#         "title": "Updated Art",
#         "artist": "Updated Artist",
#         "year": 2024,
#         "description": "Updated Description",
#         "category": category.pk,
#         "captcha": True,
#     }
#     response = client.post(url, data)
#
#     assert response.status_code == 200
#
#     updated_art = StreetArt.objects.get(pk=street_art.pk)
#
#     assert updated_art.title == "Updated Art"
#     assert updated_art.artist == "Updated Artist"
#     assert updated_art.year == 2024
#     assert updated_art.description == "Updated Description"

# @pytest.mark.django_db
# def test_add_street_art_success(client, location, category, user):
#     url = "/streetart/new/"
#     client.force_login(user)  # Logowanie użytkownika
#     response = client.post(url, {
#         "title": "Test Art",
#         "artist": "Test Artist",
#         "year": 2023,
#         "description": "Test Description",
#         "category": category,
#         "location": location,
#         "captcha": True,
#     })
#     art = StreetArt.objects.get(title="Test Art")
#     assert art.title == "Test Art"
#     assert response.status_code == 200  # Sprawdź status odpowiedzi po przekierowaniu
#
#     # Sprawdź, czy przekierowanie nastąpiło na stronę szczegółów nowo dodanego StreetArt
#     assert response.redirect_chain == [(reverse("art-detail", kwargs={"art_pk": art.pk}), 302)]


#
# @pytest.mark.django_db
# def test_create_street_art_post_success(create_street_art_view, user, category, location):
#     factory = RequestFactory()
#     request = factory.post(reverse("art-create"), data={
#         "title": "Test Art",
#         "artist": "Test Artist",
#         "year": 2023,
#         "description": "Test Description",
#         # "category": category,
#         # "location": location,
#         # "longitude": 0.0,
#         # "latitude": 0.0,
#         "captcha": True,
#     })
#     request.user = user  # Dodaj użytkownika do żądania
#     response = create_street_art_view(request)
#     assert response.status_code == 200
#     assert StreetArt.objects.count() == 1
#     art = StreetArt.objects.first()
#     assert art.title == "Test Art"
#     assert response.url == reverse("art-detail", kwargs={"art_pk": art.pk})
#
#


