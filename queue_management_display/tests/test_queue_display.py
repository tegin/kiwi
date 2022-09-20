# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestQueueDisplay(TransactionCase):
    def setUp(self):
        super().setUp()
        self.group_1 = self.env["queue.location.group"].create({"name": "G1"})
        self.group_2 = self.env["queue.location.group"].create({"name": "G2"})
        self.group_3 = self.env["queue.location.group"].create({"name": "G3"})
        self.location_1 = self.env["queue.location"].create(
            {"name": "L1", "group_ids": [(4, self.group_1.id), (4, self.group_3.id)]}
        )
        self.location_2 = self.env["queue.location"].create(
            {"name": "L2", "group_ids": [(4, self.group_2.id), (4, self.group_3.id)]}
        )

        self.token_l1 = self.env["queue.token"].create(
            {"location_ids": [(0, 0, {"location_id": self.location_1.id})]}
        )
        self.token_l2 = self.env["queue.token"].create(
            {"location_ids": [(0, 0, {"location_id": self.location_2.id})]}
        )
        self.token_g1 = self.env["queue.token"].create(
            {"location_ids": [(0, 0, {"group_id": self.group_1.id})]}
        )
        self.token_g2 = self.env["queue.token"].create(
            {"location_ids": [(0, 0, {"group_id": self.group_2.id})]}
        )
        self.token_g3 = self.env["queue.token"].create(
            {"location_ids": [(0, 0, {"group_id": self.group_3.id})]}
        )

    def test_call_exception_no_location(self):
        """
        We ensure that an error is raised if there is no location to call with.
        """
        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.action_call()

    def test_calling_error_assigned(self):
        """
        If we try to call a token that is already assigned, an error will be raised.
        """
        self.token_g1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        with self.assertRaises(ValidationError):
            self.token_g1.location_ids.with_context(
                location_id=self.location_1.id
            ).action_call()

    def test_call_wrong_location(self):
        """
        We are expecting an error if I try to call a token from a wrong location.
        """
        with self.assertRaises(ValidationError):
            self.token_g1.location_ids.with_context(
                location_id=self.location_2.id
            ).action_call()

        with self.assertRaises(ValidationError):
            self.token_l1.location_ids.with_context(
                location_id=self.location_2.id
            ).action_call()

    def test_call_correct(self):
        """
        We expect that the action cal works properly.
        """
        self.assertFalse(self.token_l1.location_ids.last_call)
        self.assertFalse(self.token_l1.location_ids.expected_location_id)
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_call()
        self.assertTrue(self.token_l1.location_ids.last_call)
        self.assertEqual(
            self.token_l1.location_ids.expected_location_id, self.location_1
        )

    def test_call_only_one(self):

        self.token_g3.location_ids.with_context(
            location_id=self.location_1.id
        ).action_call()

        self.assertEqual(
            self.token_g3.location_ids.expected_location_id, self.location_1
        )

        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_call()

        self.assertFalse(self.token_g3.location_ids.expected_location_id)
        self.assertEqual(
            self.token_l1.location_ids.expected_location_id, self.location_1
        )
