from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from users.forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'reg.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        self.send_mail_ls(email)
        return super().form_valid(form)

    def send_mail_ls(self, email):
        send_mail(
            'Регистрация',
            'Добро пожаловать на сайт!',
            'foodgram.ru <admin@foodgram.ru>',
            [email],
            fail_silently=False
        )
