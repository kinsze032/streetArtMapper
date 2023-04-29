from django.db import models


CATEGORIES = (
    (1, "mural"),
    (2, "graffiti"),
    (3, "instalacja"),
    (4, "neon"),
)   # jako model zrobić.


class StreetArt(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE) # oneToOne
    # rated_by_users = models.ManyToManyField(User, through='StreetArtUserRating')
    #można się odwołać do listy Street Artu ocenionego przez użytkownika

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.IntegerField(choices=CATEGORIES)


class Location(models.Model):
    city = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.DecimalField(max_digits=8, decimal_places=6)

    def __str__(self):
        return f"{self.city}"


# class StreetArtUserRating(models.Model):
#     street_art = models.ForeignKey(StreetArt, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField()
