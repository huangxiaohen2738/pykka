import unittest
import uuid

from pykka import Actor

class ActorInterruptTest(unittest.TestCase):
    def setUp(self):
        class ActorWithInterrupt(Actor):
            def _event_loop(self):
                raise KeyboardInterrupt
        self.actor = ActorWithInterrupt()

    def test_issuing_keyboard_interrupt_stops_process(self):
        try:
            self.actor._run()
            self.fail('Should throw SystemExit exception')
        except SystemExit:
            pass

class ActorReactTest(unittest.TestCase):
    def setUp(self):
        class ActorWithoutCustomReact(Actor):
            pass
        self.actor = ActorWithoutCustomReact()

    def test_sending_unexpected_message_raises_not_implemented_error(self):
        try:
            self.actor._react({'unhandled': 'message'})
            self.fail('Should throw NotImplementedError')
        except NotImplementedError:
            pass

class ActorUrnTest(unittest.TestCase):
    def setUp(self):
        class AnyActor(Actor):
            pass
        self.actors = [AnyActor.start() for _ in range(3)]

    def tearDown(self):
        for actor in self.actors:
            actor.stop()

    def test_actor_has_an_uuid4_based_urn(self):
        self.assertEqual(4, uuid.UUID(self.actors[0].actor_urn).version)

    def test_actor_has_unique_uuid(self):
        self.assertNotEqual(self.actors[0].actor_urn, self.actors[1].actor_urn)
        self.assertNotEqual(self.actors[1].actor_urn, self.actors[2].actor_urn)
        self.assertNotEqual(self.actors[2].actor_urn, self.actors[0].actor_urn)
