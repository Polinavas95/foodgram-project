from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from users.models import User
from django import forms


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

        def form_valid(self, form):
            email = form.cleaned_data['email']
            self.send_mail_ls(email)
            return super().form_valid(form)

        def send_mail_ls(self, email):
            send_mail(
                'Регистрация',
                'Регистрация прошла успешно!',
                'foodgram.ru <admin@foodgram.ru>',
                [email],
                fail_silently=False
            )


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
