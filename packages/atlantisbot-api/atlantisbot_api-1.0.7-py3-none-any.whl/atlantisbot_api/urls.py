from django.urls import path
from django.conf.urls import include

from rest_framework import permissions, routers

from .api import views as discord_views

router = routers.DefaultRouter()

router.register(r'raids', discord_views.RaidsStateViewSet)
router.register(r'users', discord_views.DiscordUserViewSet)
router.register(r'amigosecreto', discord_views.AmigoSecretoPersonViewSet)
router.register(r'amigosecreto_status', discord_views.AmigoSecretoStatusViewSet)
router.register(r'disabled_commands', discord_views.DisabledCommandViewSet)
router.register(r'ingame_names', discord_views.DiscordIngameNameViewSet)
router.register(r'doacoes', discord_views.DoacaoViewSet)
router.register(r'doacoes_goals', discord_views.DoacaoGoalViewSet)

urlpatterns = [
    path('api/oauth/authorize/', discord_views.DiscordOauthAuthorizeView.as_view()),
    path('api/oauth/user/', discord_views.DiscordUserOauthView.as_view()),
    path('api/', include(router.urls))
]
