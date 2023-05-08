"""
URL configuration for streetArtMapper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from artbase.views import HomeView, StreetArtDetailView, StreetArtListView
from artbase.views import StreetArtSearchView
from artbase.views import CreateReviewView, CreateStreetArtView, EditStreetArtView, ReportArtView
from artbase.views import profile, LoginView, LogoutView

urlpatterns = [
    # path('accounts/',
    #      include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('streetart/<int:art_pk>/', StreetArtDetailView.as_view(), name='art-detail'),
    path('streetart/list/', StreetArtListView.as_view(), name='art-list'),
    path('streetart/search/', StreetArtSearchView.as_view(), name='art-search'),
    path('streetart/<int:art_pk>/review/new/', CreateReviewView.as_view(), name='review-create'),
    path('streetart/<int:art_pk>/reviews/<int:review_pk>/', CreateReviewView.as_view(), name='review-edit'),
    path('streetart/new/', CreateStreetArtView.as_view(), name='art-create'),
    path('streetart/<int:art_pk>/edit/', EditStreetArtView.as_view(), name='art-edit'),
    path('streetart/zglos-streetart/', ReportArtView.as_view(), name='report-art'),
]

