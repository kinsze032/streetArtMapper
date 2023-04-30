from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
import folium
from folium.plugins import FastMarkerCluster

from artbase.models import StreetArt, Category, Location


class HomeView(View):
    def get(self, request):
        arts = StreetArt.objects.all()

        # create a Folium map centered on Katowice
        map = folium.Map(location=[50.26480752, 19.02348142], zoom_start=12)

        # add a marker to the map for each street art
        for art in arts:
            coordinates = (art.location.latitude, art.location.longitude)
            popup_html = f"<a href='/streetart/{art.id}' target='_blank'>{art.title} ({art.category.get_type_display()})</a>"

            if art.category.get_type_display() == "mural":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(map)
            if art.category.get_type_display() == "neon":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(map)
            if art.category.get_type_display() == "graffiti":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="green", icon="info-sign")
                ).add_to(map)
            if art.category.get_type_display() == "instalacja":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="darkpurple", icon="info-sign")
                ).add_to(map)

        #use FastMarerCluster to generate the clusters on the map
        #to do this, we pass list of all(lat, lon) tuples in the data
        # latitudes = [art.location.latitude for art in arts]
        # longitudes = [art.location.longitude for art in arts]
        #
        # FastMarkerCluster(data=list(zip(latitudes, longitudes))).add_to(map)

        context = {'map': map._repr_html_()}
        return render(request, "artbase/main.html", context)


class StreetArtDetailView(View):
    pass


class StreetArtListView(View):
    def get(self, request):
        streetarts = StreetArt.objects.all()
        context = {'streetarts': streetarts}
        return render(request, 'artbase/streetart_list.html', context)
