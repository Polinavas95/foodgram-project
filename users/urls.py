from django.urls import path
from users.views import SignUp

app_name = 'users'


urlpatterns = [
    path('reg/', SignUp.as_view(), name='registration', ),
]

