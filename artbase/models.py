from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def art_file_path(instance, filename):
    return "art-photo/{}/{}".format(instance.street_art.id, filename)


class StreetArt(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    location = models.OneToOneField('Location', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class StreetArtPhoto(models.Model):
    street_art = models.ForeignKey(StreetArt, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, upload_to=art_file_path)


class Category(models.Model):
    class ArtworkType(models.IntegerChoices):
        MURAL = 1, 'mural'
        GRAFFITI = 2, 'graffiti'
        INSTALACJA = 3, 'instalacja'
        NEON = 4, 'neon'

    type = models.IntegerField(choices=ArtworkType.choices)

    def __str__(self):
        return self.get_type_display()

    def get_type_name(self):
        return self.ArtworkType(self.type).name


class Location(models.Model):
    city = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.city


class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    art = models.ForeignKey(StreetArt, on_delete=models.CASCADE)
