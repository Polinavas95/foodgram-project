from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.forms import SignUpForm


User = get_user_model()


class SignUp(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('recipes:index')
    template_name = 'users/reg.html'

