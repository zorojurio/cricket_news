from django.urls import path
from marketing.views import email_list_signup


urlpatterns = [
    path('subscribe/', email_list_signup, name='subscribe'),

]
