# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import freezegun

from odoo import api
from odoo.tests.common import TransactionCase


class TestTokenLocationAction(TransactionCase):
    def setUp(self):
        super().setUp()
        self.registry.enter_test_mode(self.env.cr)
        self.env = api.Environment(
            self.registry.test_cr, self.env.uid, self.env.context
        )
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

    def tearDown(self):
        self.registry.leave_test_mode()
        super().tearDown()

    def test_token_location_back_to_draft_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_back_to_draft()
        action = self.token_l1.action_view_log()
        last_row = self.env[action["res_model"]].search(
            action["domain"], limit=1, order="id desc"
        )
        self.assertEqual(last_row.action, "back_to_draft")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location_id.id, self.token_l1.location_ids.id)
        self.assertEqual(last_row.location_id.id, self.location_1.id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)

    def test_token_location_leave_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_assign()
        action = self.token_l1.action_view_log()
        last_row = self.env[action["res_model"]].search(action["domain"], limit=1)
        self.assertEqual(last_row.action, "assign")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location_id.id, self.token_l1.location_ids.id)
        self.assertEqual(last_row.location_id.id, self.location_1.id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)
        # Also, we check the display name in this point
        self.assertIn(self.token_l1.name, last_row.display_name)
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_leave()
        action = self.token_l1.action_view_log()
        last_row = self.env[action["res_model"]].search(
            action["domain"], limit=1, order="id desc"
        )
        self.assertEqual(last_row.action, "leave")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location_id.id, self.token_l1.location_ids.id)
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
        action = self.token_l1.action_view_log()
        last_row = self.env[action["res_model"]].search(
            action["domain"], limit=1, order="id desc"
        )
        self.assertEqual(last_row.action, "cancel")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location_id.id, self.token_l1.location_ids.id)
        self.assertEqual(last_row.location_id.id, self.location_1.id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)

    def test_token_location_reopen_action(self):
        self.token_l1.location_ids.with_context(
            location_id=self.location_1.id
        ).action_cancel()
        self.token_l1.location_ids.action_reopen_cancelled()
        action = self.token_l1.action_view_log()
        last_row = self.env[action["res_model"]].search(
            action["domain"], limit=1, order="id desc"
        )
        self.assertEqual(last_row.action, "reopen")
        self.assertEqual(last_row.token_id.id, self.token_l1.id)
        self.assertEqual(last_row.token_location_id.id, self.token_l1.location_ids.id)
        self.assertFalse(last_row.location_id)
        self.assertTrue(last_row.date)
        self.assertEqual(last_row.user_id.id, self.env.user.id)

    def test_token_location_action_delete(self):
        with freezegun.freeze_time("2020-01-01"):
            self.token_l1.location_ids.with_context(
                location_id=self.location_1.id
            ).action_cancel()
        action = self.token_l1.action_view_log()
        self.assertTrue(self.env[action["res_model"]].search(action["domain"]))
        self.env["queue.token.location.action"].autovacuum()
        self.env[action["res_model"]].refresh()
        self.assertFalse(self.env[action["res_model"]].search(action["domain"]))
