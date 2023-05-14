import pytest
from django.contrib.auth.models import User
from artbase.models import Category, Location, StreetArt, StreetArtPhoto, Review
from artbase.views import CreateStreetArtView, HomeView


@pytest.fixture
def user():
    return User.objects.create(username="test_user", password="test_pwd")


@pytest.fixture
def category():
    return Category.objects.create(type=Category.ArtworkType.MURAL)


@pytest.fixture
def location():
    return Location.objects.create(
        city="Test City",
        longitude=12.34567,
        latitude=23.45678,
    )


@pytest.fixture
def street_art():
    category = Category.objects.create(type=Category.ArtworkType.MURAL)
    location = Location.objects.create(city="Test City", longitude=12.34567, latitude=23.45678)
    return StreetArt.objects.create(
        title="Test Art",
        artist="Test Artist",
        year=2023,
        description="Test Description",
        category=category,
        location=location,
    )


@pytest.fixture
def street_art_photo(street_art):
    return StreetArtPhoto.objects.create(
        street_art=street_art,
        photo=f'art-photo/{street_art.id}/test_photo.jpg',
        thumbnail=f'art-photo/{street_art.id}/test_thumbnail.jpg',
    )


@pytest.fixture
def review(user, street_art):
    return Review.objects.create(
        content='Test Review',
        rating=5,
        creator=user,
        art=street_art,
    )


@pytest.fixture
def create_street_art_view(user):
    return CreateStreetArtView.as_view()


@pytest.fixture
def home_view():
    return HomeView.as_view()
