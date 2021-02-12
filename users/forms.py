from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.core.mail import send_mail
from django.forms import forms
from django.shortcuts import render, redirect

from foodgram import settings
from users.models import User


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

    def send_mail(self, request, **kwargs):
        subject = "Для заверешния регистрации подтвердите почту"

        if request.method == "POST":
            try:
                user = User.objects.get(email=str(request.POST['email']))
                if user.is_active and subject and self.message and self.recipient:
                    send_mail(subject=subject,
                              message=self.message,
                              from_email=settings.EMAIL_HOST,
                              auth_user=request.user.email,
                              auth_password=request.user.password,
                              recipient_list=[self.recipient],
                              fail_silently=False)
                    print('Сообщение отправлено!')
                return render(request, self.template_name)
            except user.DoesNotExist:
                return redirect('password_reset')
