# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import mock

from odoo.tests.common import Form, TransactionCase

model = "odoo.addons.base_report_to_printer.models.printing_server"


class TestQueueEscpos(TransactionCase):
    def setUp(self):
        super().setUp()
        self.server = self.env["printing.server"].create({})
        self.printer = self.env["printing.printer"].create(
            {
                "name": "Printer",
                "server_id": self.server.id,
                "system_name": "Sys Name",
                "default": True,
                "status": "unknown",
                "status_message": "Msg",
                "model": "res.users",
                "location": "Location",
                "uri": "URI",
            }
        )
        self.token_1 = self.env["queue.token"].create({})

    @mock.patch("%s.cups" % model)
    def test_print_ticket(self, cups):
        action = self.token_1.action_print_escpos()
        self.assertEqual("queue.token.print.escpos", action["res_model"])
        wizard = (
            self.env[action["res_model"]].with_context(**action["context"]).create({})
        )
        self.assertTrue(wizard.printer_id)
        self.assertEqual(wizard.printer_id, self.printer)
        cups.Connection().printFile.assert_not_called()
        wizard.print_escpos()
        cups.Connection().printFile.assert_called_once()

    def test_printer_not_defined(self):
        self.env["printing.printer"].create(
            {
                "name": "Printer",
                "server_id": self.server.id,
                "system_name": "Sys Name",
                "default": True,
                "status": "unknown",
                "status_message": "Msg",
                "model": "res.users",
                "location": "Location",
                "uri": "URI",
            }
        )
        action = self.token_1.action_print_escpos()
        f = Form(self.env[action["res_model"]].with_context(**action["context"]))
        # We cannot save the form, so we do it this way.
        self.assertFalse(f.printer_id)

    def test_printer_forced(self):
        self.env["printing.printer"].create(
            {
                "name": "Printer",
                "server_id": self.server.id,
                "system_name": "Sys Name",
                "default": True,
                "status": "unknown",
                "status_message": "Msg",
                "model": "res.users",
                "location": "Location",
                "uri": "URI",
            }
        )
        self.env.user.printing_printer_id = self.printer
        action = self.token_1.action_print_escpos()
        with Form(self.env[action["res_model"]].with_context(**action["context"])) as f:
            self.assertTrue(f.printer_id)
            self.assertEqual(f.printer_id, self.printer)

    def test_printer_context_forced(self):
        printer = self.env["printing.printer"].create(
            {
                "name": "Printer",
                "server_id": self.server.id,
                "system_name": "Sys Name",
                "default": True,
                "status": "unknown",
                "status_message": "Msg",
                "model": "res.users",
                "location": "Location",
                "uri": "URI",
            }
        )
        self.env.user.printing_printer_id = self.printer
        action = self.token_1.action_print_escpos()
        with Form(
            self.env[action["res_model"]].with_context(
                printer_escpos_id=printer.id, **action["context"]
            )
        ) as f:
            self.assertTrue(f.printer_id)
            self.assertEqual(f.printer_id, printer)
