from .models import (
    AmigoSecretoPerson,
    AmigoSecretoState,
    DisabledCommand,
    DiscordIngameName,
    DiscordUser,
    RaidsState,
    Team,
    Player,
    AdvLogState,
    BotMessage,
    Doacao,
    DoacaoGoal,
    VoiceOfSeren
)
from django.contrib import admin

admin.site.register(AmigoSecretoState)
admin.site.register(AmigoSecretoPerson)
admin.site.register(DiscordUser)
admin.site.register(DisabledCommand)
admin.site.register(DiscordIngameName)
admin.site.register(RaidsState)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(AdvLogState)
admin.site.register(BotMessage)
admin.site.register(Doacao)
admin.site.register(DoacaoGoal)
admin.site.register(VoiceOfSeren)
