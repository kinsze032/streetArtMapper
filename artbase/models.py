from django.db import models


class StreetArt(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    location = models.OneToOneField('Location', on_delete=models.CASCADE)
    # rated_by_users = models.ManyToManyField(User, through='StreetArtUserRating')
    #można się odwołać do listy Street Artu ocenionego przez użytkownika

    def __str__(self):
        return f"{self.title} - {self.category}"


class Category(models.Model):
    class ArtworkType(models.IntegerChoices):
        MURAL = 1, 'mural'
        GRAFFITI = 2, 'graffiti'
        INSTALACJA = 3, 'instalacja'
        NEON = 4, 'neon'

    type = models.IntegerField(choices=ArtworkType.choices)

    def __str__(self):
        return self.get_type_display()


class Location(models.Model):
    city = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.city


# class StreetArtUserRating(models.Model):
#     street_art = models.ForeignKey(StreetArt, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField()
