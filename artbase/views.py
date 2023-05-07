import folium
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from artbase.forms import SearchForm, ReviewForm, StreetArtForm
from artbase.models import StreetArt, Category, Review, Location


class HomeView(View):
    def get(self, request):
        arts = StreetArt.objects.all()

        # create a Folium map centered on Katowice
        map = folium.Map(location=[50.26480752, 19.02348142], zoom_start=12)

        # add a marker to the map for each street art
        for art in arts:
            coordinates = (art.location.latitude, art.location.longitude)
            popup_html = f"<a href='/streetart/{art.id}' target='_blank'><strong>{art.title}</strong></a>"

            if art.category.get_type_display() == "mural":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="red", icon="paint-brush", prefix="fa"),
                    tooltip="Kliknij po więcej informacji",
                ).add_to(map)
            if art.category.get_type_display() == "neon":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="blue", icon="lightbulb", prefix="fa"),
                    tooltip="Kliknij po więcej informacji",
                ).add_to(map)
            if art.category.get_type_display() == "graffiti":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="green", icon="eyedropper", prefix="fa"),
                    tooltip="Kliknij po więcej informacji",
                ).add_to(map)
            if art.category.get_type_display() == "instalacja":
                folium.Marker(
                    coordinates,
                    popup=popup_html,
                    icon=folium.Icon(color="darkpurple", icon="star"),
                    tooltip="Kliknij po więcej informacji",
                ).add_to(map)

        context = {"map": map._repr_html_()}
        return render(request, "artbase/main.html", context)


class StreetArtListView(View):
    def get(self, request):
        street_arts = StreetArt.objects.all()
        art_with_reviews = []
        for art in street_arts:
            reviews = art.review_set.all()
            if reviews:
                art_rating = reviews.aggregate(Avg("rating"))['rating__avg']
                number_of_reviews = len(reviews)
            else:
                art_rating = None
                number_of_reviews = 0

            art_with_reviews.append(
                {
                    "art": art,
                    "art_rating": art_rating,
                    "number_of_reviews": number_of_reviews,
                }
            )
        context = {"art_list": art_with_reviews}
        return render(request, "artbase/streetart_list.html", context)


class StreetArtDetailView(View):
    def get(self, request, art_pk):
        art = get_object_or_404(StreetArt, pk=art_pk)
        reviews = art.review_set.all()
        if reviews:
            art_rating = reviews.aggregate(Avg("rating"))['rating__avg']
            context = {
                "art": art,
                "art_rating": art_rating,
                "reviews": reviews,
            }
        else:
            context = {
                "art": art,
                "art_rating": None,
                "reviews": None,
            }

        if request.user.is_authenticated:
            max_viewed_arts_length = 10
            viewed_arts = request.session.get('viewed_arts', [])
            # aktualnie przeglądany street art
            viewed_art = [art.id, art.title]
            if viewed_art not in viewed_arts:
                viewed_arts.insert(0, viewed_art)
            else:
                viewed_arts.remove(viewed_art)
                viewed_arts.insert(0, viewed_art)
            viewed_arts = viewed_arts[:max_viewed_arts_length]
            request.session['viewed_arts'] = viewed_arts

        return render(request, "artbase/streetart_detail.html", context)


class StreetArtSearchView(View):
    template_name = "artbase/search-results.html"
    form_class = SearchForm

    def get_arts_queryset(self, search_text, search_in):
        if search_in == "category__type":
            category_map = {
                "mural": Category.ArtworkType.MURAL,
                "instalacja": Category.ArtworkType.INSTALACJA,
                "graffiti": Category.ArtworkType.GRAFFITI,
                "neon": Category.ArtworkType.NEON,
            }
            art_type = category_map.get(search_text.lower())
            if art_type:
                return StreetArt.objects.filter(category__type=art_type)
            else:
                return StreetArt.objects.none()
        else:
            filter_kwargs = {f"{search_in}__icontains": search_text}
            return StreetArt.objects.filter(**filter_kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET)
        search_text = request.GET.get("search")
        search_in = request.GET.get("search_in", "category__type")

        context = {
            "form": form,
            "search_text": search_text,
            "search_in": search_in,
            "arts": self.get_arts_queryset(search_text, search_in)
            if search_text
            else StreetArt.objects.none(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {"form": form}
        search_text = ""
        arts = StreetArt.objects.none()

        if form.is_valid() and form.cleaned_data["search"]:
            search_text = form.cleaned_data["search"]
            search_in = form.cleaned_data.get("search_in") or "category__type"
            arts = self.get_arts_queryset(search_text, search_in)

        context["search_text"] = search_text
        context["search_in"] = search_in
        context["arts"] = arts
        return render(request, self.template_name, context)


class CreateReviewView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    permission_required = "auth.group"
    template_name = "artbase/create_update_review.html"
    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        art_pk = kwargs["art_pk"]
        review_pk = kwargs.get("review_pk")
        art = get_object_or_404(StreetArt, pk=art_pk)

        if review_pk is not None:
            review = get_object_or_404(Review, art_id=art_pk, pk=review_pk)
        else:
            review = None

        form = self.form_class(instance=review)
        context = {
            "form": form,
            "instance": review,
            "model": "Review",
            "related_instance": art,
            "related_model": "StreetArt",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        art_pk = kwargs["art_pk"]
        review_pk = kwargs.get("review_pk")
        art = get_object_or_404(StreetArt, pk=art_pk)

        if review_pk is not None:
            # Create a form to edit an existing Review, but use
            # POST data to populate the form.
            review = get_object_or_404(Review, art_id=art_pk, pk=review_pk)
            form = self.form_class(request.POST, instance=review)
        else:
            form = self.form_class(request.POST)

        # save new review or update old review
        if form.is_valid():
            # Create, but don't save the new review instance.
            updated_review = form.save(commit=False)
            # Modify revew in some way.
            updated_review.art = art
            updated_review.creator = request.user

            if review_pk is None:
                messages.success(request, 'Utworzono recenzję dla "{}".'.format(art))
            else:
                messages.success(request, 'Uaktualniono recenzję dla "{}".'.format(art))
            # Save the new instance.
            updated_review.save()
            return redirect("art-detail", art.pk)

        context = {
            "form": form,
            "instance": review,
            "model": "Review",
            "related_instance": art,
            "related_model": "StreetArt",
        }
        return render(request, self.template_name, context)


@login_required(login_url="/accounts/login/")
def profile(request):
    return render(request, "artbase/profile.html")


class CreateStreetArtView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    permission_required = "auth.group"
    template_name = "artbase/create_update_streetart.html"
    form_class = StreetArtForm

    def get(self, request, *args, **kwargs):
        context = {
            "form": self.form_class(),
            "instance": None,
            "model": "StreetArt",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            art = form.save(commit=False)
            longitude = form.cleaned_data['longitude']
            latitude = form.cleaned_data['latitude']
            user_location = f"{latitude}, {longitude}"
            geolocator = Nominatim(user_agent="artbase")  # create an object of class Nominatim
            location = geolocator.reverse(user_location, exactly_one=True)  # give the coordinates

            city = location.raw['address']['city']  # extract the city name from the result using the JSON object key
            art.location = Location.objects.create(
                city=city,
                longitude=longitude,
                latitude=latitude,
            )
            art.save()
            messages.success(request, "StreetArt został pomyślnie dodany!")
            return redirect('art-detail', art_pk=art.pk)
        else:
            context = {
                "form": form,
                "instance": StreetArt,
                "model": "StreetArt",
            }
            return render(request, self.template_name, context)


class EditStreetArtView(LoginRequiredMixin, View):
    login_url = "/accounts/login/"
    permission_required = "auth.group"
    template_name = "artbase/create_update_streetart.html"
    form_class = StreetArtForm

    def get(self, request, *args, **kwargs):
        art_pk = kwargs.get("art_pk")
        art = get_object_or_404(StreetArt, pk=art_pk)
        context = {
            "form": self.form_class(instance=art),
            "instance": art,
            "model": "StreetArt",
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        art_pk = kwargs["art_pk"]
        art = get_object_or_404(StreetArt, pk=art_pk)

        form = self.form_class(request.POST, instance=art)

        if form.is_valid():
            form.save()
            return redirect('art-detail', art_pk=art.pk)
        else:
            context = {
                "form": form,
                "instance": art,
                "model": "StreetArt",
            }
            return render(request, self.template_name, context)


class ReportArtView(View):
    template_name = 'artbase/report_art.html'

    def get(self, request):
        return render(request, self.template_name)
