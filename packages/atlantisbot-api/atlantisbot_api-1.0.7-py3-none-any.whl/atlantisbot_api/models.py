from __future__ import annotations

from random import randint

from django.db import models
from django.db.models.aggregates import Count
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from typing import Union


class DiscordIdField(models.TextField):
    description = 'A representation of a Discord ID'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super().__init__(*args, **kwargs)


class DiscordManager(models.Manager):
    def get_queryset(self):
        """
        Use the 'use_db' attribute from Model if it exists
        Used to set the Db used to be the Discord one
        https://stackoverflow.com/a/55754529/10416161
        """
        qs = super().get_queryset()

        # if `use_db` is set on model use that for choosing the DB
        if hasattr(self.model, 'use_db'):
            qs = qs.using(self.model.use_db)

        return qs

    def random(self):
        """
        Get random object from database
        https://stackoverflow.com/a/2118712/10416161
        """
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)

        return self.all()[random_index]


class DiscordEntityManager(DiscordManager):
    def by_id(self, discord_id: Union[str, int]):
        return self.filter(discord_id=str(discord_id)).first()


class DiscordModel(models.Model):
    """
    Base Model for Discord related models
    """
    objects = DiscordManager()

    class Meta:
        abstract = True


class RaidsState(DiscordModel):
    notifications = models.BooleanField(verbose_name='Notificações', default=False)
    time_to_next_message = DiscordIdField(verbose_name='Próxima Mensagem', null=True, blank=True)

    def toggle(self):
        self.notifications = not self.notifications
        self.save()

    @classmethod
    def object(cls) -> RaidsState:
        # Get the First Item
        item = cls._default_manager.first()

        # Create Item if one does not exist
        if not item:
            item = cls._default_manager.create(notifications=False)
            item.save()

        return item

    def save(self, *args, **kwargs):
        """
        https://stackoverflow.com/a/54722087/10416161
        """

        # Can't create more than one of the Model
        self.id = 1
        return super().save(*args, **kwargs)


class AdvLogState(DiscordModel):
    active = models.BooleanField(default=False)

    @classmethod
    def object(cls) -> AdvLogState:
        # Get the First Item
        item = cls._default_manager.first()

        # Create Item if one does not exist
        if not item:
            item = cls._default_manager.create(active=False)
            item.save()

        return item


class PlayerActivities(DiscordModel):
    activities_id = DiscordIdField()


class DisabledCommand(DiscordModel):
    name = models.TextField(verbose_name='Nome', unique=True)


class AmigoSecretoState(DiscordModel):
    activated = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    premio_minimo = models.BigIntegerField(null=True, blank=True)
    premio_maximo = models.BigIntegerField(null=True, blank=True)

    def toggle(self):
        self.activated = not self.activated
        self.save()

    @classmethod
    def object(cls) -> AmigoSecretoState:
        # Get the First Item
        item = cls._default_manager.first()

        # Create Item if one does not exist
        if not item:
            item = cls._default_manager.create(activated=False)
            item.save()

        return item

    def save(self, *args, **kwargs):
        """
        https://stackoverflow.com/a/54722087/10416161
        """
        # Can't create more than one of the Model
        self.id = 1
        return super().save(*args, **kwargs)


class DiscordUser(DiscordModel):
    updated = models.DateTimeField(default=timezone.now)
    warning_date = models.DateTimeField(null=True, blank=True)
    disabled = models.BooleanField(default=False)
    ingame_name = models.TextField(unique=True, null=False)
    discord_id = DiscordIdField()
    discord_name = models.TextField()

    discord = DiscordEntityManager()


@receiver(post_save, sender=DiscordUser, dispatch_uid='create_ingame_name')
def create_ingame_name(sender, instance, **kwargs):
    """
    Create new DiscordIngameName instance once a DiscordUser is first created with its ingame_name
    """
    ingame_name = DiscordIngameName(user=instance, name=instance.ingame_name)
    ingame_name.save()


class AmigoSecretoPerson(DiscordModel):
    objects = DiscordManager()

    user = models.ForeignKey(
        to=DiscordUser,
        verbose_name='Usuário',
        related_name='discord_user',
        on_delete=models.CASCADE
    )

    giving_to_user = models.ForeignKey(
        to=DiscordUser,
        verbose_name='Presenteando',
        related_name='giving_to_discord_user',
        on_delete=models.CASCADE,
        null=True
    )

    receiving = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Prevent user from rolling himself on Secret Santa
        """
        if self.user == self.giving_to_user:
            raise ValidationError('Um Usuário não pode presentear a si mesmo')

        super(AmigoSecretoPerson, self).save(*args, **kwargs)


class DiscordIngameName(DiscordModel):
    name = models.TextField(verbose_name='Nome RuneScape')
    created_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(
        to=DiscordUser,
        verbose_name='Usuário',
        related_name='ingame_names',
        db_column='user',
        on_delete=models.CASCADE
    )


class Team(DiscordModel):
    created_date = models.DateTimeField(default=timezone.now)
    team_id = models.CharField(unique=True, max_length=100)
    title = models.CharField(max_length=300)
    size = models.IntegerField()
    role = DiscordIdField(null=True, blank=True)
    role_secondary = DiscordIdField(null=True, blank=True)
    author_id = DiscordIdField()
    invite_channel_id = DiscordIdField()
    invite_message_id = DiscordIdField()
    team_channel_id = DiscordIdField()
    team_message_id = DiscordIdField()
    secondary_limit = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return (
            f'Team(title={repr(self.title)}, '
            f'author={repr(self.author_id)}, '
            f'team_channel_id={repr(self.team_channel_id)})'
        )


class VoiceOfSeren(DiscordModel):
    current_voice_one = models.CharField(max_length=50)
    current_voice_two = models.CharField(max_length=50)
    message_id = DiscordIdField()
    updated = models.DateTimeField(default=timezone.now)

    @classmethod
    def object(cls) -> VoiceOfSeren:
        # Get the First Item
        return cls._default_manager.first()


class Player(DiscordModel):
    player_id = DiscordIdField()
    role = DiscordIdField(null=True, blank=True)
    in_team = models.BooleanField(default=False)
    substitute = models.BooleanField(default=False)
    secondary = models.BooleanField(default=False)

    team = models.ForeignKey(
        to=Team,
        verbose_name='Time',
        related_name='players',
        db_column='team',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f'Player(team={repr(self.team)}, '
            f'player_id={repr(self.player_id)})'
        )


class BotMessage(DiscordModel):
    message_id = DiscordIdField(unique=True)
    team = models.ForeignKey(
        to=Team,
        verbose_name='Time',
        related_name='bot_messages',
        db_column='team',
        on_delete=models.CASCADE
    )


class Doacao(models.Model):
    doador_name = models.TextField(max_length=12)
    date = models.DateTimeField(default=timezone.now)
    amount = models.BigIntegerField()


class DoacaoGoal(models.Model):
    goal = models.BigIntegerField()
    active = models.BooleanField(default=False)
    name = models.TextField()
