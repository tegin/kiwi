# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import Form, TransactionCase


class TestQueueTokenSequence(TransactionCase):
    def test_queue_token_sequence_new(self):

        self.env["ir.sequence"].search([("code", "=", "queue.token")]).write(
            {"prefix": "MyToken"}
        )

        with Form(self.env["queue.token"]) as f:
            self.assertEqual(f.name, "New")
            token = f.save()
        self.assertNotEqual(token.name, "New")
        self.assertTrue(token.name.startswith("MyToken"))

    def test_queue_token_forced(self):
        token = self.env["queue.token"].create({"name": "My forced token"})
        self.assertEqual(token.name, "My forced token")
