from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django.views import View

import folium
from artbase.models import StreetArt


class HomeView(View):
    def get(self, request):
        arts = StreetArt.objects.all()

        # create a Folium map centered on Katowice
        map = folium.Map(location=[50.26480752, 19.02348142], zoom_start=12)

        # add a marker to the map for each street art
        for art in arts:
            coordinates = (art.location.latitude, art.location.longitude)
            popup_html = f"<a href='/streetart/{art.id}' target='_blank'>{art.title} ({art.category.get_type_display()})</a>"

            if art.category.get_type_display() == 'mural':
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(map)
            if art.category.get_type_display() == 'neon':
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(map)
            if art.category.get_type_display() == 'graffiti':
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color='green', icon='info-sign')
                ).add_to(map)
            if art.category.get_type_display() == 'instalacja':
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color='darkpurple', icon='info-sign')
                ).add_to(map)

        context = {'map': map._repr_html_()}
        return render(request, 'artbase/main.html', context)


class StreetArtListView(View):
    def get(self, request):
        streetarts = StreetArt.objects.all()
        art_with_reviews = []
        for art in streetarts:
            reviews = art.review_set.all()
            if reviews:
                art_rating = reviews.aggregate(Avg('rating'))
                number_of_reviews = len(reviews)
            else:
                art_rating = None
                number_of_reviews = 0

            art_with_reviews.append({
                'art': art,
                'art_rating': art_rating,
                'number_of_reviews': number_of_reviews,
            })
        context = {'art_list': art_with_reviews}
        return render(request, 'artbase/streetart_list.html', context)


class StreetArtDetailView(View):
    def get(self, request, pk):
        art = get_object_or_404(StreetArt, pk=pk)
        reviews = art.review_set.all()
        if reviews:
            art_rating = reviews.aggregate(Avg('rating'))
            context = {
                'art': art,
                'art_rating': art_rating,
                'reviews': reviews,
            }
        else:
            context = {
                'art': art,
                'art_rating': None,
                'reviews': None,
            }
        return render(request, 'artbase/streetart_detail.html', context)


class StreetArtSearchView(View):
    def get(self, request):
        search_text = request.GET.get("search", "")
        return render(request, "artbase/search-results.html", {"search_text": search_text})

