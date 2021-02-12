from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from importlib._common import _

from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import CreateView, FormView

from users.forms import CreationForm, LoginForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'reg.html'

    def form_valid(self, form):
        valid = super().form_valid(form)
        login(self.request, self.object)
        return valid


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "authForm.html", {"form": form})

        user = authenticate(request, **form.cleaned_data)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            form.add_error("username", "Аккаунт отключен")
            return render(request, "authForm.html", {"form": form})
        form.add_error("username", "Неверный логин или пароль")
        return render(request, "authForm.html", {"form": form})
    form = LoginForm()
    return render(request, "authForm.html", {"form": form})


def password_change(request):
    old_password = request.POST['old_password ']
    new_password1 = request.POST['new_password1']
    new_password2 = request.POST['new_password2']
    if old_password != new_password1 and old_password != new_password2:
        return password_change(request, post_change_redirect='changePassword.html')
    return


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['old_password'] = self.request.old_password
        kwargs['new_password1'] = self.request.new_password1
        kwargs['new_password2'] = self.request.new_password2
        return kwargs

    def form_valid(self, form):
        if self.request.old_password != self.request.new_password1 and self.request.old_password != self.request.new_password2:
            form.save()
            update_session_auth_hash(self.request, form.user)
            return super().form_valid(form)
        return redirect("password_change")
