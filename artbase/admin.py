from django.contrib import admin

from artbase.models import StreetArt, Location, Category, Review


class StreetArtAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "year", "description", "category", "location")
    list_filter = ("category",)
    search_fields = ("title", "artist", "location__city")


class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "longitude", "latitude")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["type"]


class ReviewAdmin(admin.ModelAdmin):
    date_hierarchy = "date_created"
    list_display = ("content", "rating", "date_created", "date_edited", "creator", "art")
    list_filter = ("creator", "date_created")


admin.site.register(StreetArt, StreetArtAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
