from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from django.templatetags.static import static
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, \
    PasswordChangeDoneView, PasswordResetDoneView, PasswordResetCompleteView

from cosmicdb.views import CosmicLoginView, CosmicSignupView, CosmicPasswordResetView, \
    CosmicPasswordResetConfirmView, CosmicPasswordChangeView, \
    Home, Dashboard, notifications, messages, CosmicChangeEmail

favicon_view = RedirectView.as_view(url=static('cosmicdb/img/favicon.ico'), permanent=True)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', CosmicLoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^password_change/$', CosmicPasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change_done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password_reset/$', CosmicPasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset_done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]+-[0-9A-Za-z]+)/$',CosmicPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^password_reset_complete/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^email_change/$', login_required(CosmicChangeEmail.as_view()), name='email_change'),
    url(r'^favicon\.ico$', favicon_view, name='favicon_default'),
    url(r'^$', Home.as_view(), name='home'),
    url(r'^dashboard/$', login_required(Dashboard.as_view()), name='dashboard'),
    url(r'^notifications/$', notifications, name='notifications'),
    url(r'^notifications/(?P<id>[0-9]+)/$', notifications, name='notifications'),
    url(r'^messages/$', messages, name='messages'),
    url(r'^messages/(?P<id>[0-9]+)/$', messages, name='messages'),
]

if hasattr(settings, 'COSMICDB_ALLOW_SIGNUP'):
    if settings.COSMICDB_ALLOW_SIGNUP:
        urlpatterns = urlpatterns + [
            url(r'^signup/$', CosmicSignupView.as_view(), name='signup'),
        ]
