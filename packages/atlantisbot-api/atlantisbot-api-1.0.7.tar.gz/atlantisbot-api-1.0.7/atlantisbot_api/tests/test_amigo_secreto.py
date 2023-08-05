from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import AmigoSecretoState, AmigoSecretoPerson, DiscordUser


class AmigoSecretoStateTestCase(TestCase):
    def test_first_state(self):
        state = AmigoSecretoState.object()

        self.assertIsNotNone(state)
        self.assertTrue(isinstance(state.activated, bool))

    def test_state_toggle(self):
        state = AmigoSecretoState.object()

        first_state = state.activated
        state.toggle()
        self.assertNotEqual(first_state, state.activated)

    def test_only_one_state(self):
        state = AmigoSecretoState.object()
        state.activated = False
        state.save()

        new_state = AmigoSecretoState(activated=True)
        new_state.save()

        self.assertEqual(new_state.id, 1)
        self.assertEqual(state.id, new_state.id)


class AmigoSecretoPersonTestCase(TestCase):
    def setUp(self):
        self.user_1 = DiscordUser(discord_id='1', ingame_name='name_1', discord_name='name#1')
        self.user_2 = DiscordUser(discord_id='2', ingame_name='name_2', discord_name='name#2')
        self.user_1.save()
        self.user_2.save()

    def test_same_giver_and_receiver(self):
        giver = AmigoSecretoPerson(user=self.user_1, giving_to_user=self.user_1)

        with self.assertRaises(ValidationError):
            giver.save()

    def test_giver_and_receiver(self):
        giver = AmigoSecretoPerson(user=self.user_1, giving_to_user=self.user_2)
        giver.save()
