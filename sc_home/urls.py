from django.urls import path
from sc_home import views

app_name = "home"

urlpatterns = [
    path("", views.welcome,name="welcome"),
    path("contact_us", views.contact,name="contact")
]