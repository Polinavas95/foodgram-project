from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_view
from django.contrib.flatpages import views as flatpages_views
from django.urls import include, path

app_name = 'foodgram'

handler400 = 'recipes.views.page_bad_request'  # noqa
handler404 = 'recipes.views.page_not_found'  # noqa
handler500 = 'recipes.views.server_error'  # noqa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('recipes.urls')),
    path('api/', include('api.urls')),
]

urlpatterns += [
    path('auth/', include([
            path('login/', auth_view.LoginView.as_view(
                template_name='registration/login.html'), name='login'),
            path('logout/', auth_view.LogoutView.as_view(
                template_name='registration/logged_out.html'), name='logout'),
            path('password-change/', auth_view.PasswordChangeView.as_view(
                template_name='registration/password_change_form.html'
            ), name='password_change'),
            path('password-change/done/',
                 auth_view.PasswordChangeDoneView.as_view(
                    template_name='registration/password_change_done.html'
                    ), name='password_change_done'),
            path('password-reset/',
                 auth_view.PasswordResetView.as_view(
                    template_name='registration/password_reset_form.html'
                    ), name='password_reset'),
            path('reset/<uidb64>/<token>/',
                 auth_view.PasswordResetConfirmView.as_view(
                    template_name='registration/password_reset_confirm.html'
                    ), name='password_reset_confirm'),
            path('password-reset/done/',
                 auth_view.PasswordResetDoneView.as_view(
                    template_name='registration/password_reset_done.html'
                    ), name='password_reset_done'),
        ])),
]

urlpatterns += [
    path('about/about-author/', flatpages_views.flatpage,
         {'url': '/about-author/'}, name='about-author'),
    path('about/about-spec/', flatpages_views.flatpage,
         {'url': '/about-spec/'}, name='about-spec'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
