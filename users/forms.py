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

    def save(self, commit=True):
        user = super(CreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        user.set_password(self.cleaned_data['password1'])
        message = "Пожалуйста пройдите по ссылке ниже"
        send_mail(self, message, from_email=settings.EMAIL_HOST_USER, recipient_list=user.email)
        # Save this session without saving in database
        if commit:
            user.save()
        return user

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
                              recipient_list=self.recipient,
                              fail_silently=False)
                return render(request, self.template_name)
            except user.DoesNotExist:
                return redirect('password_reset')
