from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('aboutus/', views.AboutUsPageView.as_view(), name='aboutus'),
    path('faq/', views.FAQPageView.as_view(), name='faq'),
    path('terms/', views.TermsPageView.as_view(), name='terms'),

]
