# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestLocationKanban(TransactionCase):
    def setUp(self):
        super().setUp()

        self.location_1 = self.env["queue.location"].create(
            {"name": "L1", "group_ids": []}
        )
        self.location_2 = self.env["queue.location"].create(
            {"name": "L2", "group_ids": []}
        )
        self.location_3 = self.env["queue.location"].create(
            {"name": "L3", "group_ids": []}
        )

        self.token_l1 = self.env["queue.token"].create(
            {"location_ids": [(0, 0, {"location_id": self.location_1.id})]}
        )
        self.token_l2 = self.env["queue.token"].create(
            {"location_ids": [(0, 0, {"location_id": self.location_2.id})]}
        )

    def test_location_kanban_field_waiting(self):
        self.assertEqual(self.location_3.state, "waiting")

    def test_location_kanban_fields(self):
        self.assertEqual(self.location_1.state, "warning")
        self.assertFalse(self.location_1.current_token_location_id)
        self.assertEqual(1, self.location_1.token_location_count)
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.location_1.refresh()
        self.assertEqual(self.location_1.state, "working")
        self.assertEqual(
            self.location_1.current_token_location_id, self.token_l1.location_ids
        )
        self.assertEqual(1, self.location_1.token_location_count)
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_leave()
        self.location_1.refresh()
        self.assertEqual(self.location_1.state, "waiting")
        self.assertFalse(self.location_1.current_token_location_id)
        self.assertEqual(0, self.location_1.token_location_count)
