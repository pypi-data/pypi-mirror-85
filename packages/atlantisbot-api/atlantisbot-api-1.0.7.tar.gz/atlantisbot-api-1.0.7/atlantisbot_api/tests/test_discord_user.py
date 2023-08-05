from django.test import TestCase

from ..models import DiscordUser, DiscordIngameName


class DiscordUserTestCase(TestCase):
    test_discord_id = '123456789'
    test_ingame_name = 'some name'
    test_discord_name = 'DiscordName#123'

    def setUp(self):
        test_user = DiscordUser(
            discord_id=self.test_discord_id,
            ingame_name=self.test_ingame_name,
            discord_name=self.test_discord_name
        )
        test_user.save()
        self.test_user = test_user

    def test_by_discord_id(self):
        test_user = DiscordUser.discord.by_id(self.test_discord_id)

        self.assertIsNotNone(test_user)
        self.assertEqual(test_user.discord_id, self.test_discord_id)
        self.assertEqual(test_user.ingame_name, self.test_ingame_name)

    def test_created_ingame_name(self):
        ingame_name = DiscordIngameName.objects.filter(name=self.test_ingame_name).first()

        self.assertIsNotNone(ingame_name)
        self.assertEqual(ingame_name.name, self.test_ingame_name)
        self.assertEqual(self.test_user.id, ingame_name.user.id)
