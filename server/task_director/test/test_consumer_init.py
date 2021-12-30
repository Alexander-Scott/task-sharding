import asyncio
import json

from django.test import TestCase

from task_director.src.controller import TaskDirectorController
from task_director.src.message_type import MessageType

from task_director.test.mock_classes.mock_consumer import MockConsumer


class TaskDirectorTests__SingleConsumerInit(TestCase):
    def setUp(self):
        self.controller = TaskDirectorController()
        self.consumer_id = "UUID1"
        self.consumer = MockConsumer(self.consumer_id)
        self.controller.register_consumer(self.consumer_id, self.consumer)

    def test__when_one_consumer_connected__expect_server_to_return_msg(self):
        """
        GIVEN a freshly instantiated TaskDirectorController.
        WHEN a consumer connects and sends an init message with a single step.
        EXPECT the server to return to the same consumer a build instruction message.
        """

        mock_client_init_msg = {
            "message_type": MessageType.INIT,
            "branch": "master",
            "cache_id": "1",
            "schema_id": "1",
            "total_steps": 1,
        }

        expected_server_build_msg = {
            "message_type": MessageType.BUILD_INSTRUCTION,
            "schema_id": "1",
            "step_id": "0",
        }

        asyncio.get_event_loop().run_until_complete(
            self.controller.handle_received(mock_client_init_msg, self.consumer_id)
        )

        actual_server_build_msg = json.loads(self.consumer.get_sent_data())

        self.assertDictEqual(expected_server_build_msg, actual_server_build_msg)


class TaskDirectorTests__TwoConsumersInit(TestCase):
    def setUp(self):
        self.controller = TaskDirectorController()
        self.consumer_id_1 = "UUID1"
        self.consumer_1 = MockConsumer(self.consumer_id_1)
        self.controller.register_consumer(self.consumer_id_1, self.consumer_1)
        self.consumer_id_2 = "UUID2"
        self.consumer_2 = MockConsumer(self.consumer_id_2)
        self.controller.register_consumer(self.consumer_id_2, self.consumer_2)

    def test__when_two_consumers_connected__expect_server_to_return_two_msgs(self):
        """
        GIVEN a freshly instantiated TaskDirectorController.
        WHEN two consumers connect and send INIT messages with two steps.
        EXPECT the server to return to the first consumer a build instruction for the first step,
          AND the server to return to the second consumer a build instruction for the second step.
        """

        mock_client_init_msg = {
            "message_type": MessageType.INIT,
            "branch": "master",
            "cache_id": "1",
            "schema_id": "1",
            "total_steps": 2,
        }
        expected_server_build_msg_1 = {
            "message_type": MessageType.BUILD_INSTRUCTION,
            "schema_id": "1",
            "step_id": "1",
        }
        expected_server_build_msg_2 = {
            "message_type": MessageType.BUILD_INSTRUCTION,
            "schema_id": "1",
            "step_id": "0",
        }

        asyncio.get_event_loop().run_until_complete(
            self.controller.handle_received(mock_client_init_msg, self.consumer_id_1)
        )
        actual_server_build_msg_1 = json.loads(self.consumer_1.get_sent_data())
        asyncio.get_event_loop().run_until_complete(
            self.controller.handle_received(mock_client_init_msg, self.consumer_id_2)
        )
        actual_server_build_msg_2 = json.loads(self.consumer_2.get_sent_data())

        self.assertDictEqual(expected_server_build_msg_1, actual_server_build_msg_1)
        self.assertDictEqual(expected_server_build_msg_2, actual_server_build_msg_2)

    def test__when_two_consumer_connected__and_cache_id_is_incompatible__expect_two_schema_director_instances_created(
        self,
    ):
        """
        GIVEN a freshly instantiated TaskDirectorController.
        WHEN two consumers connect and send INIT messages with one step,
          AND each consumer has a different cache ID.
        EXPECT a build instruction message with the same step ID to be sent to each consumer.
        """
        mock_client_init_msg_1 = {
            "message_type": MessageType.INIT,
            "branch": "master",
            "cache_id": "1",
            "schema_id": "1",
            "total_steps": 1,
        }
        mock_client_init_msg_2 = {
            "message_type": MessageType.INIT,
            "branch": "master",
            "cache_id": "2",
            "schema_id": "1",
            "total_steps": 1,
        }
        expected_server_build_msg_1 = {
            "message_type": MessageType.BUILD_INSTRUCTION,
            "schema_id": "1",
            "step_id": "0",
        }
        expected_server_build_msg_2 = {
            "message_type": MessageType.BUILD_INSTRUCTION,
            "schema_id": "1",
            "step_id": "0",
        }

        asyncio.get_event_loop().run_until_complete(
            self.controller.handle_received(mock_client_init_msg_1, self.consumer_id_1)
        )
        actual_server_build_msg_1 = json.loads(self.consumer_1.get_sent_data())
        asyncio.get_event_loop().run_until_complete(
            self.controller.handle_received(mock_client_init_msg_2, self.consumer_id_2)
        )
        actual_server_build_msg_2 = json.loads(self.consumer_2.get_sent_data())

        self.assertDictEqual(expected_server_build_msg_1, actual_server_build_msg_1)
        self.assertDictEqual(expected_server_build_msg_2, actual_server_build_msg_2)
