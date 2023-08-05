from django.test import TestCase

from ..models import RaidsState


class RaidsStateTestCase(TestCase):
    def test_first_state(self):
        state = RaidsState.object()

        self.assertIsNotNone(state)
        self.assertTrue(isinstance(state.notifications, bool))

    def test_state_toggle(self):
        state = RaidsState.object()

        first_state = state.notifications
        state.toggle()
        self.assertNotEqual(first_state, state.notifications)

    def test_only_one_state(self):
        state = RaidsState.object()
        state.notifications = False
        state.save()

        new_state = RaidsState(notifications=True)
        new_state.save()

        self.assertEqual(new_state.id, 1)
        self.assertEqual(state.id, new_state.id)
