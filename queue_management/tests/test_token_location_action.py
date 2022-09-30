# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestTokenLocationAction(TransactionCase):

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


    def test_token_location_assign_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        last_row = self.env["queue.token.location.action"].search([])[-1]
        self.assertEqual(last_row.action , "assign")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location.id, self.token_l1.location_ids.id)
        self.assertEqual(last_row.location_id.id, self.location_1.id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)

    def test_token_location_back_to_draft_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_back_to_draft()
        last_row = self.env["queue.token.location.action"].search([])[-1]
        self.assertEqual(last_row.action , "back_to_draft")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location.id, self.token_l1.location_ids.id)
        self.assertEqual(last_row.location_id.id, self.location_1.id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)

    def test_token_location_leave_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_leave()
        last_row = self.env["queue.token.location.action"].search([])[-1]
        self.assertEqual(last_row.action , "leave")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location.id, self.token_l1.location_ids.id)
        self.assertEqual(last_row.location_id.id, self.location_1.id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)

    def test_token_location_cancel_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_cancel()
        last_row = self.env["queue.token.location.action"].search([])[-1]
        self.assertEqual(last_row.action , "cancel")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location.id, self.token_l1.location_ids.id)
        self.assertEqual(last_row.location_id.id, self.location_1.id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)

    def test_token_location_reopen_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_cancel()
        self.token_l1.location_ids.action_reopen_cancelled()
        last_row = self.env["queue.token.location.action"].search([])[-1]
        self.assertEqual(last_row.action , "reopen")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location.id, self.token_l1.location_ids.id)
        self.assertFalse(last_row.location_id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)
